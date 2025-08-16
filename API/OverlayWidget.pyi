from PySide6.QtWidgets import QWidget
from typing import Optional, Any

from API.config import Config
from Common.core import APIBaseWidget
from API.PluginSetting import PluginSettingWidget
from ApiPlugins.widgetPreloader import WidgetPreLoader


class OverlayWidget(QWidget, APIBaseWidget):
    """
    Базовый виджет-оверлей с поддержкой тем и конфигурации.

    """
    
    dumper: WidgetPreLoader
    
    def __init__(self, config: Config, parent: Optional[QWidget] = None) -> None:
        """
        Инициализирует оверлейный виджет.

        :param Config config: Конфигурация виджета
        :param Optional[QWidget] parent: Родительский виджет
        """
        ...
    
    def reloadConfig(self) -> None:
        """
        Перезагружает конфигурацию виджета.
        """
        ...
    
    def savesConfig(self) -> dict[str, Any]:
        """
        Возвращает текущее состояние для сохранения.

        :return dict[str, Any]: Словарь с сохраняемыми параметрами.
        :note: В базовой реализации возвращает пустой словарь
        """
        ...
    
    def restoreConfig(self, config: dict[str, Any]) -> None:
        """
        Восстанавливает состояние из конфигурации.

        :param dict[str, Any] config: Ранее сохранённые параметры.
        :note: В базовой реализации не делает ничего
        """
        ...
    
    def loader(self) -> None:
        """
        Основной метод загрузки содержимого виджета.

        :note: Предназначен для переопределения в дочерних классах
        """
        ...
    
    def loadConfig(self) -> None:
        """
        Загружает конфигурацию стилей и тем.
        """
        ...
    
    @classmethod
    def createSettingWidget(
            cls,
            widget: "OverlayWidget",
            name_plugin: str,
            parent: QWidget
    ) -> PluginSettingWidget:
        """
        Создаёт виджет настроек для этого виджета-оверлея.

        :param OverlayWidget widget: Экземпляр виджета
        :param str name_plugin: Имя плагина
        :param QWidget parent: Родительский виджет.
        :return PluginSettingWidget: Виджет настроек
        """
        ...