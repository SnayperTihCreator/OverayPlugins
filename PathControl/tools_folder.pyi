import sys

class ToolsIniter:
    """Инициализатор путей к инструментам платформы"""
    def __init__(self, name: str = "tools") -> None: ...
    def load(self) -> None:
        """
        Добавляет платформо-специфичные пути в sys.path.
        Создает директории common, windows и linux если их нет.
        """
        ...