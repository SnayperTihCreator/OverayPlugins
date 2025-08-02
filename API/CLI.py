from typing import Callable

from PySide6.QtWidgets import QWidget


class MetaCliInterface(type(QWidget)): ...


class CLInterface(metaclass=MetaCliInterface):
    cliFunction: dict[str, Callable]
    
    @staticmethod
    def register(name: str = None) -> Callable: ...
    
    def namespace(self): ...
