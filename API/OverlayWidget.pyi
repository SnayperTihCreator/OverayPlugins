from PySide6.QtWidgets import QWidget
from API.config import Config
from API.core import APIBaseWidget
from API.PluginSetting import PluginSettingWidget


class OverlayWidget(QWidget, APIBaseWidget):
    """
    Базовый класс для оверлейных виджетов (накладываемых поверх других окон).

    Предоставляет базовый функционал для:
    - Работы с конфигурацией
    - Создания виджета настроек
    - Сериализации/десериализации состояния
    """
    
    def __init__(self, config: Config, parent: QWidget = None) -> None:
        """
        Инициализирует оверлейный виджет.

        Args:
            config: Конфигурация виджета
            parent: Родительский виджет
        """
        ...
    
    def reloadConfig(self) -> None:
        """Перезагружает конфигурацию и обновляет состояние виджета."""
        ...
    
    def savesConfig(self) -> dict:
        """
        Возвращает текущее состояние виджета для сохранения.

        Returns:
            dict: Пустой словарь (должен быть переопределен в дочерних классах)
        """
        ...
    
    def restoreConfig(self, config: dict) -> None:
        """
        Восстанавливает состояние виджета из конфигурации.

        Args:
            config: Словарь с настройками
        """
        ...
    
    def loader(self) -> None:
        """Загружает/обновляет состояние виджета (должен быть реализован в потомках)."""
        ...
    
    @classmethod
    def createSettingWidget(
            cls,
            widget: "OverlayWidget",
            name_plugin: str,
            parent: QWidget
    ) -> PluginSettingWidget:
        """
        Создает виджет настроек для данного оверлейного виджета.

        Args:
            widget: Экземпляр OverlayWidget
            name_plugin: Имя плагина
            parent: Родительский виджет

        Returns:
            PluginSettingWidget: Виджет с настройками
        """
        ...