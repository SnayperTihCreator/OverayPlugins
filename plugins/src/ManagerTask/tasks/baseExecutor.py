from abc import abstractmethod
from typing import Any

from PySide6.QtCore import Signal, QRunnable, QThreadPool, Slot
from attrs import define, field

from .core import QABCObject





@define(slots=False)
class BaseExecutor(QABCObject):
    display_name = "<unknown>"
    
    result: Any = field(default=None, init=False)
    error: str = field(default="", init=False)
    
    finished = Signal(bool)
    
    def __attrs_post_init__(self):
        super().__init__()
    
    def clear(self):
        self.result = None
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> bool:
        """Метод выполнения"""
        pass
    
    def __call__(self):
        task = ExecutorTask(self)
        QThreadPool.globalInstance().start(task)
        return True
    
    @classmethod
    @abstractmethod
    def getGUI(cls):
        """Метод получения GUI"""
        pass
    
    @property
    @abstractmethod
    def description(self):
        """Описание исполнителя"""
        pass


class ExecutorTask(QRunnable):
    def __init__(self, executor: BaseExecutor):
        super().__init__()
        self.setAutoDelete(True)
        self.executor = executor
    
    @Slot()
    def run(self, /):
        try:
            self.executor.execute()
            self.executor.finished.emit(True)
        except Exception as e:
            self.executor.error = str(e)
            self.executor.finished.emit(False)
    