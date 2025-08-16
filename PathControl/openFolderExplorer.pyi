from pathlib import Path


def open_file_manager(path: Path) -> None:
    """
    Открывает файловый менеджер системы для указанного пути.

    :param path: Путь к папке для открытия
    :raises FileNotFoundError: Если путь не существует
    :raises OSError: Для неподдерживаемых ОС
    :note: Поддерживает Windows и Linux
    """
    ...