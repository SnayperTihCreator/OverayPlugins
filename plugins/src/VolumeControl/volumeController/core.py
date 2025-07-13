from abc import ABC, abstractmethod
from typing import Callable, Any

from attrs import define, field


@define
class Application:
    name: str
    pid: int
    _session: Any = field(repr=False)
    
    def _on_get_mute(self):
        pass
    
    def _on_set_mute(self, value):
        pass
    
    @property
    def mute(self):
        return self._on_get_mute()
    
    @mute.setter
    def mute(self, value):
        self._on_set_mute(value)
        
    def _on_get_volume(self):
        pass
    
    def _on_set_volume(self, value):
        pass
    
    @property
    def volume(self):
        return self._on_get_volume()
    
    @volume.setter
    def volume(self, value):
        self._on_set_volume(value)


@define
class SystemVolume(Application):
    pid: int = field(default=-1, init=False, repr=False)
    name: str = field(default="System", init=False)


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
    def set_application_mute(self, app_id: int, muted: bool):
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