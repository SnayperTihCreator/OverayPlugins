from fs.base import FS
from fs.opener import Opener
from abc import abstractmethod
from contextvars import ContextVar
from contextlib import contextmanager

_current_plugin: ContextVar[str] = ...


def isActiveContextPlugin() -> bool:
    """Проверяет активен ли контекст плагина."""
    ...


@contextmanager
def contextPlugin(pluginName: str):
    """
    Контекстный менеджер для временной установки контекста плагина.

    :param pluginName: Имя плагина
    """
    ...


class BasePathOpener(Opener):
    """Базовый класс для открытия файловых систем"""
    
    @abstractmethod
    def getImplFS(self, url: str, parse_result, writable: bool, create: bool, cwd: str) -> FS: ...