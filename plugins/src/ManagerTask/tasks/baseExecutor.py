from abc import abstractmethod
from typing import Any

from attrs import define, field

from .core import ABCObject


@define
class BaseExecutor(ABCObject):
    result_execute: Any = field(default=None)
    
    def clear(self):
        self.result_execute = None
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> bool: pass
