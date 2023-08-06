import logging

from ..Interfaces.DefaultInterface import DefaultInterface
from . import BaseSource, Sources

log = logging.getLogger(__name__)

log.debug("Loading module")


@Sources.register("VariantSource")
class VariantSource(BaseSource.BaseSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.debug("init %s", self.key)

        self.interface = DefaultInterface
