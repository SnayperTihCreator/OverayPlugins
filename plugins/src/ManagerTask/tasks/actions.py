from enum import Enum, auto
from typing import Any
import yaml
from attrs import define, field
from PySide6.QtCore import Signal

from .core import QABCObject, registry_to_yaml, registry_from_yaml
from .baseTriggers import BaseTrigger
from .baseExecutor import BaseExecutor


class ActionStatus(Enum):
    IDLE = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    CANCELLED = auto()
    
    @classmethod
    def to_yaml(cls, dumper: yaml.Dumper, data):
        return dumper.represent_scalar("!ActionStatus", str(data.value))
    
    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node):
        data = loader.construct_scalar(node)
        return cls(int(data))


registry_to_yaml(ActionStatus, ActionStatus.to_yaml)
registry_from_yaml("!ActionStatus", ActionStatus.from_yaml)


@define(slots=False)
class Action(QABCObject):
    """Упрощённая реализация Action с Qt-интеграцией"""
    
    # Qt сигналы
    status_changed = Signal(ActionStatus)
    error_occurred = Signal(str)
    
    executor: BaseExecutor = field()
    trigger: BaseTrigger = field()
    status: ActionStatus = field(default=ActionStatus.IDLE, init=False)
    _error: str = field(default=None, init=False)
    _result: Any = field(default=None, init=False)
    
    def __attrs_post_init__(self):
        super().__init__()  # Инициализация QObject
    
    def cancel(self):
        """Оригинальная логика с сигналами"""
        self.trigger.stop()
        self._update_status(ActionStatus.CANCELLED)
    
    def restart(self):
        self.trigger.stop()
        self.executor.clear()
        self._error = ""
        self._result = None
        self._update_status(ActionStatus.IDLE)
    
    def update(self):
        if self.is_finish():
            return
        
        if self.status == ActionStatus.IDLE:
            self._update_status(ActionStatus.RUNNING)
            self.trigger.start()
        
        if self.trigger():
            success = self.executor()
            self._result = self.executor.result
            self._error = self.executor.error
            self._update_status(ActionStatus.SUCCESS if success else ActionStatus.CANCELLED)
            
            if self._error:
                self.status = ActionStatus.FAILED
                self.error_occurred.emit(self._error)
    
    def _update_status(self, new_status):
        """Обновление статуса с уведомлением"""
        if self.status != new_status:
            self.status = new_status
            self.status_changed.emit(new_status)
    
    # Оригинальные методы без изменений
    def is_finish(self):
        return self.status in {ActionStatus.SUCCESS, ActionStatus.FAILED, ActionStatus.CANCELLED}
    
    def get_error(self):
        return self._error
    
    def get_result(self):
        return self._result
    
    @classmethod
    def restore(cls, data):
        obj = cls(data["executor"], data["trigger"])
        obj.status = data["status"]
        obj._error = data.get("error")
        return obj
    
    def save(self):
        return {
            "executor": self.executor,
            "trigger": self.trigger,
            "status": self.status,
            "error": self._error
        }