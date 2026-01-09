from abc import abstractmethod
from attrs import define, field

from OExtension.yaml_storage import YamlSerialized


class BaseTrigger(YamlSerialized):
    display_name = "<unknown>"
    
    # Сигналы для триггеров
    
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


@define
class AndTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
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


@define
class OrTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
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
