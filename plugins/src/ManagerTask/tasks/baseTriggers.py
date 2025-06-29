from abc import abstractmethod
from PySide6.QtCore import Signal
from attrs import define, field

from .core import QABCObject


class BaseTrigger(QABCObject):
    display_name = "<unknown>"
    
    # Сигналы для триггеров
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def stop(self):
        self.clearTrig()
    
    def clearTrig(self):
        """Очистка состояния триггера"""
        pass
    
    @abstractmethod
    def __call__(self) -> bool:
        """Проверка условия триггера"""
        pass
    
    def start(self):
        """Активация триггера"""
        pass
    
    @classmethod
    @abstractmethod
    def getGUI(cls):
        """Получение GUI для настройки триггера"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание триггера"""
        pass


@define(slots=False)
class AndTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
    def __attrs_post_init__(self):
        super().__init__()
    
    def clearTrig(self):
        for trigger in self.triggers:
            trigger.clearTrig()
    
    def stop(self):
        for trigger in self.triggers:
            trigger.stop()
    
    def __call__(self) -> bool:
        return all(trigger() for trigger in self.triggers)
    
    @classmethod
    def restore(cls, data):
        return cls(triggers=data["triggers"])
    
    def save(self):
        return {
            "triggers": self.triggers
        }
    
    def start(self):
        for trigger in self.triggers:
            trigger.start()
    
    @classmethod
    def getGUI(cls):
        return None
    
    @property
    def description(self) -> str:
        return "&".join(trig.description for trig in self.triggers)
    
    def add(self, obj: BaseTrigger):
        if isinstance(obj, BaseTrigger):
            self.triggers.append(obj)
            return True
        return False


@define(slots=False)
class OrTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
    def __attrs_post_init__(self):
        super().__init__()
    
    def clear(self):
        for trigger in self.triggers:
            trigger.clearTrig()
    
    def stop(self):
        for trigger in self.triggers:
            trigger.stop()
    
    def __call__(self) -> bool:
        return any(trigger() for trigger in self.triggers)
    
    @classmethod
    def restore(cls, data):
        return cls(triggers=data["triggers"])
    
    def save(self):
        return {
            "triggers": self.triggers,
        }
    
    def start(self):
        for trigger in self.triggers:
            trigger.start()
    
    @classmethod
    def getGUI(cls):
        return None
    
    @property
    def description(self) -> str:
        return "|".join(trig.description for trig in self.triggers)
    
    def add(self, obj: BaseTrigger):
        if isinstance(obj, BaseTrigger):
            self.triggers.append(obj)
            return True
        return False


__all__ = ["BaseTrigger", "AndTrigger", "OrTrigger"]
