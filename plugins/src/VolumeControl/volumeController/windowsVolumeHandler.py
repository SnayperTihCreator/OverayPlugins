from threading import Thread
from typing import Callable
from ctypes import cast, POINTER

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioSessionNotification, IAudioSessionManager2
from comtypes import CLSCTX_ALL, COMObject

from .coreWin import SystemVolume, Application
from .core import BaseVolumeHandler


class AudioSessionNotifier(COMObject):
    _com_interfaces_ = [IAudioSessionNotification]
    
    def __init__(self, callback):
        self.callback = callback
        super().__init__()
    
    def OnSessionCreated(self, new_session):
        """Вызывается при создании новой аудио сессии"""
        if self.callback:
            self.callback(0, "session_created", new_session)
        return 0


class WindowsVolumeHandler(BaseVolumeHandler):
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        speaker_volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        self.gaps: dict[int, Application] = {-1: SystemVolume(speaker_volume)}
        self.gaps[-1].callback = self._handle_audio_event
        
        self.loadSession()
        
        interface = devices.Activate(IAudioSessionManager2._iid_, CLSCTX_ALL, None)
        self.session_manager = cast(interface, POINTER(IAudioSessionManager2))
        self._handler_session = None
        
        self._callback = None
    
    def loadSession(self):
        for session in AudioUtilities.GetAllSessions():
            if session.Process and session.Process.name():
                self.gaps[session.ProcessId] = Application(session.Process.name(), session.ProcessId, session)
                self.gaps[session.ProcessId].callback = self._handle_audio_event
    
    def get_applications(self) -> list[Application]:
        return [volum for idx, volum in self.gaps.items()]
    
    def set_application_volume(self, app_id: int, volume: float):
        self.gaps[app_id].volume = volume
    
    def set_application_mute(self, app_id: int, muted: bool):
        self.gaps[app_id].mute = muted
    
    def get_system_volume(self) -> float:
        return self.gaps[-1].volume
    
    def set_system_volume(self, volume: float):
        self.gaps[-1].volume = volume
    
    def get_system_mute(self) -> bool:
        return self.gaps[-1].mute
    
    def set_system_mute(self, muted: bool):
        self.gaps[-1].mute = muted
    
    def close(self):
        self.stop_monitoring()
        self.gaps.clear()
    
    def start_monitoring(self, callback: Callable[[], None]):
        self._callback = callback
        # self._handler_session = AudioSessionNotifier(self._handle_audio_event)
        # self.session_manager.RegisterSessionNotification(self._handler_session)
        
    def _handle_audio_event(self, pid, event_type, *args):
        print(pid, event_type, args)
    
    def stop_monitoring(self):
        self._callback = None
        # self.session_manager.UnregisterSessionNotification(self._handler_session)
    
    def update(self) -> bool:
        sessions = AudioUtilities.GetAllSessions()
        
        if len(sessions) == (len(self.gaps)-1): return False
        for session in sessions:
            if session.ProcessId in self.gaps: continue
            
            self.gaps[session.ProcessId] = Application(session.Process.name(), session.ProcessId, session)
            self.gaps[session.ProcessId].callback = self._handle_audio_event
        return True
