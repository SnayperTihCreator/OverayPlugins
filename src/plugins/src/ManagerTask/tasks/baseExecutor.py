from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QRunnable, QThreadPool, Slot, QTimer
from attrs import define, field

from OExtension.yaml_storage import YamlSerialized
from .signals import Signal


@define(slots=False)
class BaseExecutor(YamlSerialized):
    display_name = "<unknown>"
    
    result: Any = field(default=None, init=False)
    error: str = field(default="", init=False)
    
    finished = Signal(bool)
    
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
            self._finished(True)
        except Exception as e:
            self.executor.error = str(e)
            self._finished(False)
    
    def _finished(self, status):
        
        def invoke():
            self.executor.finished(status)
        
        QTimer.singleShot(0, invoke)
