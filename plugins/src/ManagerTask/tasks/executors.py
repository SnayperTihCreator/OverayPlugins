from pathlib import Path
from functools import partial

from attrs import define, field
from PySide6.QtCore import qWarning, QMetaObject, Q_ARG, Signal

from .baseExecutor import BaseExecutor
from .utils import run_detached
from .guiExecutors import *


@define(slots=False)
class RunCommandExecutor(BaseExecutor):
    display_name = "Run command"
    
    command: str = field(default="")
    _is_messageCheck: bool = field(default=False)
    _dialog: DialogConfirmCommand = field(default=None, init=False, repr=False)
    
    error_raised = Signal(int, str)
    result_changed = Signal(object)
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._dialog = DialogConfirmCommand(10)
        
        self.error_raised.connect(self.actOnSetError)
        self.result_changed.connect(self.actOnSetResult)
        
    def actOnSetError(self, rcode, error):
        qWarning(f"Error {rcode}: {error}")
        self.error = error
        
    def actOnSetResult(self, result):
        self.result = result
    
    def show_warring(self, title, msg):
        self._dialog.setTextData(title, msg)
        return self._dialog.exec()
    
    @property
    def description(self):
        return self.command
    
    @classmethod
    def getGUI(cls):
        widget = WidgetRunCommandExecutor()
        return widget, partial(widget.callback, cls)
    
    def execute(self):
        run_detached(self.command, self.error_raised.emit, self.result_changed.emit, False)
        
    def __call__(self):
        if self._is_messageCheck:
            btn = self.show_warring("Предупреждение", f"Вы хотите запустить: {self.command}")
            if btn:
                return super().__call__()
            else:
                return False
        else:
            return super().__call__()
    
    @classmethod
    def restore(cls, data):
        obj = cls(data["command"])
        obj._is_messageCheck = data["message_check"]
        return obj
    
    def save(self):
        return {
            "command": self.command,
            "message_check": self._is_messageCheck
        }


@define(slots=False)
class RunAppExecutor(BaseExecutor):
    display_name = "Run app with parameters"
    
    filePath: Path = field(default=Path())
    args: str = field(default="")
    
    error_raised = Signal(int, str)
    result_changed = Signal(object)
    
    def execute(self):
        run_detached(f"{self.filePath} {self.args}", self.error_raised.emit, self.result_changed.emit, False)
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self.error_raised.connect(self.actOnSetError)
        self.result_changed.connect(self.actOnSetResult)
    
    def actOnSetError(self, rcode, error):
        qWarning(f"Error {rcode}: {error}")
        self.error = error
    
    def actOnSetResult(self, result):
        self.result = result
    
    @classmethod
    def getGUI(cls):
        widget = WidgetRunAppExecutor()
        return widget, partial(widget.callback, cls)
    
    @property
    def description(self):
        return f"{self.filePath.name} :: {self.args}"
    
    @classmethod
    def restore(cls, data):
        return cls(Path(data["path"]), data["args"])
    
    def save(self):
        return {
            "path": str(self.filePath),
            "args": self.args
        }


__all__ = ["RunCommandExecutor", "RunAppExecutor"]
