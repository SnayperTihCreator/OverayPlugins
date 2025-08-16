from typing import Literal, Any
from box import Box


class Config:
    """
    Конфигурация плагина с загрузкой из TOML-файлов.

    Автоматически подгружает конфигурацию в зависимости от типа плагина.
    При ошибке загрузки использует значения по умолчанию.
    """
    
    def __init__(
            self,
            plugin_name: str,
            plugin_type: Literal["draggable_window", "overlay_widget", "apps", "setting", "theme"],
            config_name: str = "config"
    ) -> None:
        """
        Инициализирует конфигурацию для указанного типа плагина.

        :param plugin_name: Имя плагина/приложения
        :param plugin_type: Тип конфигурации
        :param config_name: Имя конфигурационного файла (без расширения)
        """
        ...
    
    def _load_config(self) -> Box[str, Any]:
        """Загружает конфигурацию из TOML-файла или возвращает значения по умолчанию."""
        ...
    
    def __getattr__(self, item: str) -> Any:
        """Проксирует доступ к атрибутам внутреннего конфига."""
        ...
    
    def reload(self) -> None:
        """Перезагружает конфигурацию из файла."""
        ...
    
    def plugin_path(self) -> str:
        """Возвращает путь к директории плагина."""
        ...
    
    @classmethod
    def configApplication(cls) -> 'Config':
        """
        Создает конфигурацию для основного приложения.

        :return: Экземпляр конфигурации с типом 'apps'
        """
        ...