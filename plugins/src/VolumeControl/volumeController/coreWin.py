from typing import Callable, Any

from comtypes import COMObject
from pycaw.pycaw import IAudioSessionEvents, IAudioEndpointVolumeCallback
from attrs import define, field

from . import core


class AudioSessionEventHandler(COMObject):
    _com_interfaces_ = [IAudioSessionEvents]
    
    def __init__(self, callback):
        self.callback = callback
        super().__init__()
    
    def OnSimpleVolumeChanged(self, new_volume, new_mute, event_context):
        """Вызывается при изменении громкости"""
        if self.callback:
            self.callback("volume_changed", new_volume, new_mute)
        return 0
    
    def OnSessionDisconnected(self, disconnect_reason):
        """Вызывается при завершении сессии"""
        if self.callback:
            self.callback("session_disconnected")
        return 0


@define
class Application(core.Application):
    callback: Callable = field(default=None, init=False, repr=False)
    _handler: Any = field(default=None, init=False, repr=False)
    
    def __attrs_post_init__(self):
        self._handler = AudioSessionEventHandler(self._on_event_session)
        self._session._ctl.RegisterAudioSessionNotification(self._handler)
    
    def _on_event_session(self, *args):
        if self.callback is not None:
            self.callback(self.pid, *args)


class AudioEndpointCallback(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]
    
    def __init__(self, callback):
        self.callback = callback
        super().__init__()
    
    def OnNotify(self, pNotify):
        """Вызывается при изменении системной громкости"""
        if self.callback:
            self.callback("system_volume_changed")
        return 0


@define
class SystemVolume(core.SystemVolume, Application):
    def __attrs_post_init__(self):
        self._handler = AudioEndpointCallback(self._on_event_session)
        self._session.RegisterControlChangeNotify(self._handler)
    
    def __del__(self):
        if self._session and self._handler:
            self._session.UnregisterControlChangeNotify(self._handler)
