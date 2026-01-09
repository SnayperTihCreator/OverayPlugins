from typing import Callable, Any

from attrs import define, field
import pulsectl

from . import core

@define
class Application(core.Application):
    callback: Callable = field(default=None, init=False, repr=False)

    def _on_get_mute(self):
        pulsectl.Pulse().client_list()

    def _on_set_mute(self, value):
        pass

    def _on_get_volume(self):
        pass

    def _on_set_volume(self, value):
        pass


@define
class SystemVolume(core.SystemVolume, Application):
    def _on_get_mute(self):
        pass

    def _on_set_mute(self, value):
        pass

    def _on_get_volume(self):
        pass

    def _on_set_volume(self, value):
        pass