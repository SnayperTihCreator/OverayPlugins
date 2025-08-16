from types import ModuleType
from abc import ABC, abstractmethod
from typing import Any

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMenu

from ApiPlugins.pluginItems import PluginItem


class PreLoader(ABC):
    """
    Абстрактный базовый класс для загрузки и сохранения состояния плагинов.

    Реализует основной функционал работы с конфигурацией плагинов.
    """
    
    @classmethod
    def saved(cls, target: Any, item: PluginItem, setting: QSettings) -> None:
        """
        Сохраняет состояние плагина в настройки.

        :param Any target: Объект плагина или None
        :param PluginItem item: Элемент плагина
        :param QSettings setting: Хранилище настроек
        :note: Сохраняет конфигурацию, активность и другие параметры
        """
        ...
    
    @classmethod
    def loaded(cls, setting: QSettings, name: str, parent: Any) -> tuple[Any, PluginItem]:
        """
        Загружает плагин из настроек.

        :param QSettings setting: Хранилище настроек
        :param str name: Имя группы настроек
        :param Any parent: Родительский объект
        :return tuple[Any, PluginItem]: Кортеж (объект плагина, элемент плагина)
        :rtype:
        :note: Восстанавливает конфигурацию и состояние активности
        """
        ...
    
    @classmethod
    @abstractmethod
    def overCreateItem(
            cls,
            module: ModuleType,
            name_type: str,
            checked: bool = False
    ) -> PluginItem:
        """
        Создает новый элемент плагина (абстрактный метод).

        :param ModuleType module: Модуль плагина
        :param str name_type: Тип плагина
        :param bool checked: Флаг активности
        :return PluginItem: Созданный элемент плагина
        """
        ...
    
    @classmethod
    @abstractmethod
    def overSaved(cls, item: PluginItem, setting: QSettings) -> None:
        """
        Дополнительные действия при сохранении (абстрактный метод).

        :param PluginItem item: Элемент плагина
        :param QSettings setting: Хранилище настроек
        """
    
    @classmethod
    @abstractmethod
    def overLoaded(cls, setting: QSettings, name: str, parent: Any) -> Any:
        """
        Дополнительные действия при загрузке (абстрактный метод).

        :param QSettings setting: Хранилище настроек
        :param str name: Имя группы
        :param Any parent: Родительский объект
        :return: Загруженный объект
        """
    
    @classmethod
    @abstractmethod
    def getParameterCreateItem(
            cls,
            setting: QSettings,
            name: str,
            parent: Any
    ) -> list[Any]:
        """
        Возвращает параметры для создания элемента (абстрактный метод).

        :param QSettings setting: Хранилище настроек
        :param str name: Имя группы
        :param Any parent: Родительский объект
        :return list[Any]: Список параметров
        """
        ...
    
    @classmethod
    @abstractmethod
    def activatedWidget(cls, state: bool, target: Any) -> None:
        """
        Обрабатывает изменение состояния активности (абстрактный метод).

        :param bool state: Новое состояние активности
        :param Any target: Объект плагина
        """
        ...
    
    @classmethod
    @abstractmethod
    def duplicate(cls, item: PluginItem) -> PluginItem:
        """
        Создает дубликат элемента плагина (абстрактный метод).

        :param PluginItem item: Исходный элемент
        :return PluginItem: Новый клон элемента
        """
        ...
    
    @classmethod
    @abstractmethod
    def createActionMenu(
            cls,
            menu: QMenu,
            widget: Any,
            item: PluginItem
    ) -> dict[str, Any]:
        """
        Создает меню действий для плагина (абстрактный метод).

        :param QMenu menu: Меню для добавления действий
        :param Any widget: Виджет плагина
        :param PluginItem item: Элемент плагина
        :return dict[str, Any]: Словарь созданных действий.
        :note: По умолчанию добавляет действия "Reload Config" и "Setting"
        """
        ...