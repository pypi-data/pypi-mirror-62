import datetime
import logging
import time
import socket

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import ModbusSocketFramer, ModbusTcpServer

from ..Shared.Internal import Statistics
from ..Sources.BaseSource import StatusCode
from ..Sources.HoldingRegisterSource import HoldingRegisterSource
from . import BaseController, Controllers


@Controllers.register("ModbusServerController")
class ModbusServerController(BaseController.BaseController):
    """
    .. tip:: Development Status :: 5 - Production/Stable

    Sequence diagram:

    .. seqdiag::

        seqdiag app{
            activation = none;
            default_note_color = LemonChiffon;
            span_height = 12;
            edge_length = 200;

            Queue [color=LemonChiffon];
            Controller [label=ModbusServerController,color=LemonChiffon];
            External [label="Pymodbus datablock",color=LemonChiffon];

            === Initialization ===
            Queue -> Controller [label="APP_STATE, SETUP"]
            === Setup ===
            Queue -> Controller [label="ADD_SOURCE, source [n]"]
            Queue -> Controller [label="APP_STATE, RUNNING"]
            === Running ===
            === Begin loop ===
            Controller <- External [
                label="Value change, register [n]",
                leftnote="
                    Update value of
                    source [n]"
            ]
            Controller -> Queue [
                label="RUN_EXPRESSION, source [n]",
                note="
                    Value change
                    in source [n]"
            ]
            ... ...
            Queue -> Controller [
                label="
                    WRITE_SOURCE,
                    source [n], value, timestamp",
                note="
                    Update value of
                    source [n]"
            ]
            Controller -> External [
                label="update value, register [n]",
                note="
                    Value change
                    in nodeid [n]"
            ]
            === End Loop ===
        }

    """

    def __init__(self, name, shared):
        super().__init__(name, shared)
        self.logger = logging.getLogger(name)
        self.logger.info("init")

    def run(self):
        "Main loop. Will exit when receiving interrupt signal"

        config = self.shared.config.config

        self.send_events_internal = config(self.name, "send_events_on_internal", 0)
        self.send_events_external = config(self.name, "send_events_on_external", 1)
        self.oldnew = config(self.name, "oldnew_comparision", 1)
        self.daemon_threads = config(self.name, "daemon_threads", 0)

        self.context = self.get_modbus_server_context()

        framer = self.get_framer()

        self.readfunction = 0x03  # read holding registers
        self.writefunction = 0x10

        identity = ModbusDeviceIdentification()
        identity.VendorName = config(self.name, "VendorName", "Pymodbus")
        identity.ProductCode = config(self.name, "ProductCode", "PM")
        identity.VendorUrl = config(
            self.name, "VendorUrl", "http://github.com/bashwork/pymodbus/"
        )
        identity.ProductName = config(self.name, "ProductName", "Pymodbus Server")
        identity.ModelName = config(self.name, "ModelName", "Pymodbus Server")
        identity.MajorMinorRevision = config(self.name, "MajorMinorRevision", "1.0")

        host = config(self.name, "host", "0.0.0.0")
        port = config(self.name, "port", 5020)

        # når vi starter modbus sin serve_forever så blokkeres denne tråden
        # og vi får ikke kjørt loop_incoming, loop_outgoing
        # vi får heller ikke signalisert shutdown.
        # ved å overstyre noen funksjoner i serveren kan vi løse dette
        # dette er gjort i MyController

        self.server = self.init_server(self.context, framer, identity, host, port)
        if self.daemon_threads:
            self.server.daemon_threads = True
        self.logger.info("listen %s, port %s", host, port)

        self.logger.info("Running")
        self.server.serve_forever()
        self.logger.info("Closing connections")
        self.server.server_close()
        self.logger.info("Stopped")

    def init_server(self, context, framer, identity, host, port):
        for i in range(20):
            if i > 0:
                time.sleep(10)
            try:
                return MyController(
                    context, framer, identity, (host, port), allow_reuse_address=True, controller=self
                )
                break
            except OSError as error:
                self.logger.error("%s. Retry in 10 sec.", repr(error))
        else:
            return MyController(
                context, framer, identity, (host, port), allow_reuse_address=True, controller=self
            )

    def get_modbus_server_context(self):
        """
        Iter the devicelist section in config-file and builds a ModbusServerContext object

        :return: an ModbusServerContext instance

        """
        config = self.shared.config.config
        device_dict = {}
        conf_device_list = config(self.name, "devicelist", self.name + "_devices")
        # self.shared.config.add_section(conf_device_list)
        devices = self.shared.config.get_dict(conf_device_list)
        for deviceconfig, deviceenabled in devices.items():
            if int(deviceenabled):
                # 'di' - Discrete Inputs initializer
                # 'co' - Coils initializer
                # 'hr' - Holding Register initializer
                # 'ir' - Input Registers iniatializer

                device_id = config(deviceconfig, "device_id", 0)
                device_name = config(deviceconfig, "device_name", "").strip("\"'")
                di_start = config(deviceconfig, "di_start", 0)
                di_length = config(deviceconfig, "di_length", 100)
                di_init_value = config(deviceconfig, "di_init_value", 0)

                co_start = config(deviceconfig, "co_start", 0)
                co_length = config(deviceconfig, "co_length", 100)
                co_init_value = config(deviceconfig, "co_init_value", 0)

                hr_start = config(deviceconfig, "hr_start", 0)
                hr_length = config(deviceconfig, "hr_length", 100)
                hr_init_value = config(deviceconfig, "hr_init_value", 0)

                ir_start = config(deviceconfig, "ir_start", 0)
                ir_length = config(deviceconfig, "ir_length", 100)
                ir_init_value = config(deviceconfig, "ir_init_value", 0)

                store = MyContext(
                    di=ModbusSequentialDataBlock(di_start, [di_init_value] * di_length),
                    co=ModbusSequentialDataBlock(co_start, [co_init_value] * co_length),
                    hr=ModbusSequentialDataBlock(hr_start, [hr_init_value] * hr_length),
                    ir=ModbusSequentialDataBlock(ir_start, [ir_init_value] * ir_length),
                    controller=self,
                    device_id=device_id,
                    device_name=device_name,
                )

                device_dict[device_id] = store

        return ModbusServerContext(slaves=device_dict, single=False)

    def get_framer(self):
        """
        Returns the framer to be used.
        Override this function to return a custom framer
        """
        return ModbusSocketFramer

    def handle_add_source(self, incoming):
        self.logger.debug("'Add source' event for %s", incoming.key)
        incoming.get = 0
        incoming.status_code = StatusCode.NONE
        self.add_source(incoming.key, incoming)

    def handle_write_source(self, incoming, value, source_time):
        if isinstance(incoming, HoldingRegisterSource):
            unit, address = incoming.unpack_unit_and_address()
            self.context[unit].setValues(self.writefunction, address, [value], True)
        self.logger.debug(
            "'Write source' event to %s. value: %s at %s",
            incoming.key,
            value,
            source_time,
        )

    def handle_datachange(self, unit, address, value, is_internal):
        name = HoldingRegisterSource.pack_unit_and_address(unit, address)

        if self.has_source(name):
            item = self.get_source(name)
            stime = datetime.datetime.utcnow()
            status_ok = True
            if self.update_source_instance_value(
                item, value, stime, status_ok, self.oldnew
            ):
                if is_internal and self.send_events_internal:
                    self.send_outgoing(item)
                elif not is_internal and self.send_events_external:
                    self.send_outgoing(item)


class MyController(ModbusTcpServer):
    daemon_threads = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = kwargs["controller"]

    def service_actions(self):
        if Statistics.on:
            Statistics.set(self.controller.name + ".clients.count", len(self.threads))
        if self.controller.has_interrupt():
            self._BaseServer__shutdown_request = True
        else:
            self.controller.loop_incoming()  # dispatch handle_* functions


class MyContext(ModbusSlaveContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = kwargs["controller"]
        self.device_id = kwargs["device_id"]
        self.device_name = kwargs["device_name"]

    def setValues(self, fx, address, values, is_internal=False):
        super().setValues(fx, address, values)
        for i, value in enumerate(values):
            self.controller.handle_datachange(
                self.device_id, address + i, value, is_internal
            )
