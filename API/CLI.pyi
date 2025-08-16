from typing import Callable

from Common.core import MetaBaseWidget


class MetaCliInterface(MetaBaseWidget): ...


class CLInterface(metaclass=MetaCliInterface):
    cliFunction: dict[str, Callable]
    
    @staticmethod
    def register(name: str = None) -> Callable: ...
    
    def namespace(self): ...
