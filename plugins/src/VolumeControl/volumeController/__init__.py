from typing import Callable

from .core import BaseVolumeHandler, Application, SystemVolume

from APIService.platformCurrent import getSystem

platform, _ = getSystem()
if platform == "win32":
    from .windowsVolumeHandler import WindowsVolumeHandler as VolumeHandler


class VolumeController(BaseVolumeHandler):
    def __init__(self):
        self.handler = VolumeHandler()
    
    def get_applications(self) -> list[Application]:
        return self.handler.get_applications()
    
    def set_application_volume(self, app_id: int, volume: float):
        self.handler.set_application_volume(app_id, volume)
    
    def set_application_mute(self, app_id: int, muted: bool):
        self.handler.set_application_mute(app_id, muted)
    
    def get_system_volume(self) -> float:
        return self.handler.get_system_volume()
    
    def set_system_volume(self, volume: float):
        self.handler.set_system_volume(volume)
    
    def get_system_mute(self) -> bool:
        return self.handler.get_system_mute()
    
    def set_system_mute(self, muted: bool):
        self.handler.set_system_mute(muted)
    
    def close(self):
        self.handler.close()
    
    def start_monitoring(self, callback: Callable[[], None]):
        self.handler.start_monitoring(callback)
    
    def stop_monitoring(self):
        self.handler.stop_monitoring()
    
    def update(self) -> bool:
        return self.handler.update()
    
    
__all__ = ["VolumeController", "Application", "SystemVolume"]