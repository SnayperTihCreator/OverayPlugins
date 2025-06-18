from abc import abstractmethod

from attrs import define, field

from .core import ABCObject


class BaseTrigger(ABCObject):
    def stop(self):
        self.clear()
    
    def clear(self):
        pass
    
    @abstractmethod
    def check(self, *args, **kwargs) -> bool:
        pass


@define
class AndTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
    def clear(self):
        for trigger in self.triggers:
            trigger.clear()
            
    def stop(self):
        for trigger in self.triggers:
            trigger.stop()
    
    def check(self, *args, **kwargs) -> bool:
        return all(trigger.check(*args, **kwargs) for trigger in self.triggers)
    
    @classmethod
    def restore(cls, data):
        return cls(data["triggers"])
    
    def save(self):
        return {"triggers": self.triggers.copy()}


@define
class OrTrigger(BaseTrigger):
    triggers: list[BaseTrigger] = field(factory=list)
    
    def clear(self):
        for trigger in self.triggers:
            trigger.clear()
    
    def stop(self):
        for trigger in self.triggers:
            trigger.stop()
    
    def check(self, *args, **kwargs) -> bool:
        return any(trigger.check(*args, **kwargs) for trigger in self.triggers)
    
    @classmethod
    def restore(cls, data):
        return cls(data["triggers"])
    
    def save(self):
        return {"triggers": self.triggers.copy()}


__all__ = ["BaseTrigger", "AndTrigger", "OrTrigger"]
