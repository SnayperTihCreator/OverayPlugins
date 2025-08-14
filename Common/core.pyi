from typing import Any
from abc import ABC, ABCMeta, abstractmethod

from box import Box
from PySide6.QtWidgets import QWidget


class MetaBaseWidget(type(QWidget), ABCMeta): ...


class APIBaseWidget(ABC, metaclass=MetaBaseWidget):
    """
    Абстрактный базовый класс для виджетов API.
    Определяет обязательный интерфейс для всех виджетов плагинов.
    """
    @abstractmethod
    def reloadConfig(self) -> None:
        """
        Абстрактный метод - должен перезагружать конфигурацию виджета.

        Raises:
            NotImplementedError: Если не реализован в дочернем классе
        """
        ...
    
    @abstractmethod
    def savesConfig(self) -> dict[str, Any]:
        """
        Возвращает текущую конфигурацию виджета для сохранения.

        Returns:
            Dict[str, Any]: Словарь с настройками виджета
        """
        ...
    
    @abstractmethod
    def restoreConfig(self, config: Box) -> None:
        """
        Абстрактный метод - должен восстанавливать состояние виджета из конфига.

        Args:
            config: Конфигурация виджета в формате Box

        Raises:
            NotImplementedError: Если не реализован в дочернем классе
        """
        ...
    
    @classmethod
    def createSettingWidget(
            cls,
            obj: "APIBaseWidget",
            name_plugin: str,
            parent: QWidget
    ) -> QWidget:
        """
        Абстрактный метод - должен создавать виджет настроек для этого виджета.

        Args:
            obj: Экземпляр виджета
            name_plugin: Имя плагина
            parent: Родительский виджет

        Returns:
            QWidget: Виджет с настройками

        Raises:
            NotImplementedError: Если не реализован в дочернем классе
        """
        ...