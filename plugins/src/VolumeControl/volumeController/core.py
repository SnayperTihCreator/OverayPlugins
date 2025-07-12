from abc import ABC, abstractmethod
from typing import Callable, Any

from attrs import define, field


@define
class Application:
    name: str
    pid: int
    _session: Any = field(repr=False)
    
    @property
    def mute(self):
        return bool(self._session.SimpleAudioVolume.GetMute())
    
    @mute.setter
    def mute(self, value):
        self._session.SimpleAudioVolume.SetMute(value, None)
    
    @property
    def volume(self):
        return self._session.SimpleAudioVolume.GetMasterVolume()
    
    @volume.setter
    def volume(self, value):
        self._session.SimpleAudioVolume.SetMasterVolume(value, None)


@define
class SystemVolume(Application):
    pid: int = field(default=-1, init=False, repr=False)
    name: str = field(default="System", init=False)
    
    @property
    def mute(self):
        return bool(self._session.GetMute())
    
    @mute.setter
    def mute(self, value):
        self._session.SetMute(value, None)
    
    @property
    def volume(self):
        return self._session.GetMasterVolumeLevelScalar()
    
    @volume.setter
    def volume(self, value):
        self._session.SetMasterVolumeLevelScalar(value, None)


class BaseVolumeHandler(ABC):
    """Абстрактный базовый класс для управления громкостью"""
    
    @abstractmethod
    def get_applications(self) -> list[Application]:
        """Получить список приложений со звуком"""
        pass
    
    @abstractmethod
    def set_application_volume(self, app_id: int, volume: float):
        """Установить громкость приложения"""
        pass
    
    @abstractmethod
    def set_application_mute(self, app_id: str, muted: bool):
        """Включить/выключить звук приложения"""
        pass
    
    @abstractmethod
    def get_system_volume(self) -> float:
        """Получить системную громкость"""
        pass
    
    @abstractmethod
    def set_system_volume(self, volume: float):
        """Установить системную громкость"""
        pass
    
    @abstractmethod
    def get_system_mute(self) -> bool:
        """Получить состояние системного звука"""
        pass
    
    @abstractmethod
    def set_system_mute(self, muted: bool):
        """Включить/выключить системный звук"""
        pass
    
    @abstractmethod
    def close(self):
        """Освободить ресурсы"""
        pass
    
    @abstractmethod
    def start_monitoring(self, callback: Callable[[], None]):
        """Начать мониторинг изменений аудиопотоков"""
        pass
    
    @abstractmethod
    def stop_monitoring(self):
        """Остановить мониторинг изменений"""
        pass
    
    @abstractmethod
    def update(self)->bool:
        """Если что-то изменилось"""
        pass


__all__ = ["Application", "SystemVolume", "BaseVolumeHandler"]