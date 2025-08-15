from typing import Any, Literal
from pathlib import Path


class Config:
    """
    Класс для работы с конфигурацией плагина в формате TOML.

    Автоматически загружает конфиг из файла <config_name>.toml рядом с указанным путем.
    Если файл не найден или поврежден, создает новый с дефолтными значениями.
    Предоставляет доступ к параметрам конфига как к атрибутам класса.
    """
    
    def __init__(
            self,
            name: str,
            plugin_type: Literal["draggable_window", "overlay_widget", "apps", "theme"],
            config_name: str = "config",
    ) -> None:
        """
        Инициализирует конфигурацию плагина.

        Args:
            name: имя ресурса
            plugin_type: Тип плагина (определяет набор дефолтных значений)
            config_name: Имя конфигурационного файла (без расширения)
            create_is_not: Создавать ли новый конфиг, если файл не найден
        """
        ...
    
    def __getattr__(self, item: str) -> Any:
        """Проксирует доступ к атрибутам внутреннего конфига."""
        ...
    
    def reload(self) -> None:
        """Перезагружает конфигурацию из файла."""
        ...
    
    def plugin_path(self) -> Path:
        """
        Возвращает путь к директории плагина.

        Returns:
            Path: Абсолютный путь к родительской директории
        """
        ...
    
    def loadFile(self, path, mode="r", data_storage="auto"): ...