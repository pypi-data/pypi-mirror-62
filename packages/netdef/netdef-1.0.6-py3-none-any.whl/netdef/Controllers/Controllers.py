import functools
import importlib
import logging
from collections import OrderedDict

CONTROLLERDICT = OrderedDict()

# denne dekoratoren vil bli aktivert av aktiverte klasser etter Controllers.load()
def register(name):
    """
    A decorator to register controllers. Example::

        from netdef.Controllers import BaseController, Controllers

        @Controllers.register("NewControllerTemplate")
        class NewControllerTemplate(BaseController.BaseController):
            def __init__(self, name, shared):
                ...
    """

    def classdecorator(name, cls):
        CONTROLLERDICT[name] = cls
        return cls

    return functools.partial(classdecorator, name)


class Controllers:
    """
    A collection of all loaded controllers
    """

    def __init__(self, shared=None):
        self.logging = logging.getLogger(__name__)
        self.items = CONTROLLERDICT
        self.add_shared_object(shared)
        self.instances = OrderedDict()

    def add_shared_object(self, shared):
        self.shared = shared

    def init(self):
        for name, class_ in self.items.items():
            self.instances[name] = class_(name, self.shared)

    def load(self, base_packages):
        """
        Imports controller modules. Creates queue instances associated with the given controllers.

        Example::
        
            from netdef.Controllers import Controllers
            controllers = Controllers.Controllers(shared)
            controllers.load([__package__, 'netdef'])

        """
        # Importerer controller-modulene. lager kø-instanser til controllermodulene
        # Gjør forberedelser slik at alle delte klasser og instanser er "på plass"
        # når instansen av kontrolleren senere blir initiert

        if isinstance(base_packages, str):
            base_packages = [base_packages]

        added = []

        for base_package in base_packages:

            activate_controllers = self.shared.config.get_dict("controllers")
            for name, activate in activate_controllers.items():
                if int(activate) and not name in added:
                    try:
                        # laster modul
                        importlib.import_module(
                            "{}.Controllers.{}".format(base_package, name)
                        )
                        # lager kø-instanser
                        added.append(name)
                    except ImportError as e:
                        if isinstance(e.name, str):
                            if not e.name.startswith(base_package + ".Controllers"):
                                raise (e)
                        else:
                            raise (e)

        for name, activate in activate_controllers.items():
            if int(activate) and not name in added:
                self.logging.error("%s not found in %s", name, base_packages)

        for name in self.items.keys():
            self.shared.queues.add_controller(name)
            self.shared.queues.send_setup_state_to_controller(name)

        activate_aliases = self.shared.config.get_dict("controller_aliases")
        for name, origin in activate_aliases.items():
            if origin in self.items:
                self.items[name] = self.items[origin]
                self.shared.queues.add_controller(name)
                self.shared.queues.send_setup_state_to_controller(name)
            else:
                self.logging.error(
                    "%s not found for alias %s in configfile", origin, name
                )
