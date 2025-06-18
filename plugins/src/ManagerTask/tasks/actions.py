from enum import Enum, auto
from typing import Any

import yaml
from attrs import define, field

from .core import ABCObject, registry_from_yaml, registry_to_yaml
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


registry_to_yaml(yaml.SafeDumper, ActionStatus, ActionStatus.to_yaml)
registry_from_yaml(yaml.SafeLoader, "!ActionStatus", ActionStatus.from_yaml)


@define
class Action(ABCObject):
    executor: BaseExecutor = field()
    trigger: BaseTrigger = field()
    status: ActionStatus = field(default=ActionStatus.IDLE, init=False)
    
    _error: str = field(repr=False, init=False, default=None)
    _result: Any = field(repr=False, init=False, default=None)
    
    def cancel(self):
        self.trigger.stop()
        self.status = ActionStatus.CANCELLED
        
    def clear(self):
        self.trigger.clear()
        self.executor.clear()
    
    def update(self, *args, **kwargs):
        if self.status in [ActionStatus.SUCCESS, ActionStatus.FAILED]:
            return
        
        if self.status == ActionStatus.IDLE:
            self.status = ActionStatus.RUNNING
        
        if self.trigger.check(*args, **kwargs):
            try:
                self.executor.execute(*args, **kwargs)
                self._result = self.executor.result_execute
                self.status = ActionStatus.SUCCESS
            except Exception as e:
                self._error = str(e)
                self.status = ActionStatus.FAILED
                
    def is_compiled(self):
        return self.status in [ActionStatus.SUCCESS, ActionStatus.FAILED]
    
    def get_error(self):
        return self._error
    
    def get_result(self):
        return self._result
    
    @classmethod
    def restore(cls, data):
        obj = cls(data["executor"], data["trigger"])
        obj.status = data["status"]
        return obj
    
    def save(self):
        return {
            "executor": self.executor,
            "trigger": self.trigger,
            "status": self.status,
            "error": str(self._error)
        }
