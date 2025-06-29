from datetime import datetime, timedelta
from functools import partial
from typing import Optional

from attrs import define, field

from .baseTriggers import BaseTrigger
from . import installation_registry
from .guiTriggers import *


@define(slots=False)
class EmptyTrigger(BaseTrigger):
    display_name = "Empty Trigger"
    
    # Сигнал срабатывания (наследуется от BaseTrigger)
    
    def __call__(self) -> bool:
        return True
    
    @classmethod
    def restore(cls, data):
        return cls()
    
    def save(self):
        return {}
    
    @classmethod
    def getGUI(cls):
        return None
    
    @property
    def description(self):
        return "Always True"


@define(slots=False)
class AbsoluteDateTimeTrigger(BaseTrigger):
    display_name = "Absolute Time Trigger"
    raise_datetime: datetime = field()
    
    def __attrs_post_init__(self):
        super().__init__()
    
    def __call__(self) -> bool:
        current_time = datetime.now().replace(microsecond=0)
        if self.raise_datetime <= current_time:
            return True
        return False
    
    @classmethod
    def restore(cls, data):
        return cls(raise_datetime=data["datetime"])
    
    def save(self):
        return {
            "datetime": self.raise_datetime,
        }
    
    @classmethod
    def getGUI(cls):
        widget = WidgetAbsoluteDateTimeTrigger()
        return widget, partial(widget.callback, cls)
    
    @property
    def description(self):
        return f"Trigger at {self.raise_datetime.isoformat()}"
    
    def set_datetime(self, new_datetime: datetime):
        """Установка нового времени срабатывания с уведомлением"""
        if self.raise_datetime != new_datetime:
            self.raise_datetime = new_datetime


@define(slots=False)
class RelativeDateTimeTrigger(BaseTrigger):
    display_name = "Relative Time Trigger"
    delta: timedelta = field()
    start_time: Optional[datetime] = field(init=False, default=None)
    
    def __call__(self) -> bool:
        if self.start_time is None:
            return False
        
        current_time = datetime.now().replace(microsecond=0)
        trigger_time = self.start_time + self.delta
        
        if trigger_time <= current_time:
            return True

        return False
    
    @classmethod
    def restore(cls, data):
        obj = cls(delta=data["delta"])
        if "start_time" in data and data["start_time"] is not None:
            obj.start_time = data["start_time"]
        return obj
    
    def save(self):
        return {
            "delta": self.delta,
            "start_time": self.start_time,
        }
    
    def start(self):
        """Активация триггера с фиксацией времени старта"""
        self.start_time = datetime.now().replace(microsecond=0)
    
    def clearTrig(self):
        """Сброс времени старта"""
        self.start_time = None
    
    @classmethod
    def getGUI(cls):
        widget = WidgetRelativeDateTimeTrigger()
        return widget, partial(widget.callback, cls)
    
    @property
    def description(self):
        return f"Trigger after {self.delta}"


__all__ = [
    "AbsoluteDateTimeTrigger",
    "RelativeDateTimeTrigger",
    "EmptyTrigger"
]