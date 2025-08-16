from abc import ABC, abstractmethod
from typing import Any

from box import Box
from PySide6.QtWidgets import QWidget


class MetaBaseWidget(type(QWidget)):
    """Метакласс для базового виджета API."""
    ...


class APIBaseWidget(QWidget, ABC, metaclass=MetaBaseWidget):
    """
    Абстрактный базовый класс для всех виджетов API.

    Обеспечивает:
    - Единый интерфейс работы с конфигурацией
    - Поддержку системы настроек
    - Типизированное взаимодействие между компонентами
    """
    
    dumper: Any  #: Класс для дампа/загрузки состояния
    config: Box  #: Конфигурация виджета
    
    @abstractmethod
    def reloadConfig(self) -> None:
        """Перезагружает конфигурацию виджета."""
        ...
    
    @abstractmethod
    def savesConfig(self) -> Box:
        """
        Возвращает текущее состояние для сохранения.

        :return: Конфигурация в формате Box
        """
        ...
    
    @abstractmethod
    def restoreConfig(self, config: Box) -> None:
        """
        Восстанавливает состояние из конфигурации.

        :param config: Ранее сохраненная конфигурация
        """
        ...
    
    @classmethod
    @abstractmethod
    def createSettingWidget(
            cls,
            obj: 'APIBaseWidget',
            name_plugin: str,
            parent: Any
    ) -> Any:
        """
        Создает виджет настроек для этого компонента.

        :param obj: Экземпляр виджета
        :param name_plugin: Имя плагина
        :param parent: Родительский виджет
        :return: Виджет настроек
        """
        ...