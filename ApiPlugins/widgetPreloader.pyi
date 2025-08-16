from types import ModuleType
from typing import Any

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMenu

from ApiPlugins.preloader import PreLoader
from ApiPlugins.pluginItems import PluginItem


class WidgetPreLoader(PreLoader):
    """
    Загрузчик виджетов плагинов.

    Реализует специфичную для виджетов логику загрузки и управления.
    Наследуется от абстрактного класса PreLoader.
    """
    
    @classmethod
    def overCreateItem(
            cls,
            module: ModuleType,
            checked: bool = False,
            **kwargs: Any
    ) -> PluginItem:
        """
        Создает элемент плагина для виджета.

        :param ModuleType module: Модуль плагина
        :param bool checked: Флаг активности
        :param kwargs: Дополнительные параметры
        :return PluginItem: Созданный элемент плагина
        """
    
    @classmethod
    def overSaved(cls, item: PluginItem, setting: QSettings) -> None:
        """
        Дополнительные действия при сохранении виджета.

        :param PluginItem item: Элемент плагина
        :param QSettings setting: Хранилище настроек
        :note: В текущей реализации не выполняет действий
        """
        ...
    
    @classmethod
    def overLoaded(cls, setting: QSettings, name: str, parent: Any) -> None:
        """
        Дополнительные действия при загрузке виджета.

        :param QSettings setting: Хранилище настроек
        :param str name: Имя группы настроек
        :param Any parent: Родительский объект
        :note: В текущей реализации не выполняет действий
        """
        ...
    
    @classmethod
    def getParameterCreateItem(
            cls,
            setting: QSettings,
            name: str,
            parent: Any
    ) -> list:
        """
        Возвращает параметры для создания элемента виджета.

        :param QSettings setting: Хранилище настроек
        :param str name: Имя группы настроек
        :param Any parent: Родительский объект
        :return list: Список параметров (в текущей реализации пустой)
        """
        ...
    
    @classmethod
    def activatedWidget(cls, state: bool, target: Any) -> None:
        """
        Обрабатывает изменение состояния активности виджета.

        :param bool state: Новое состояние активности
        :param Any target: Виджет плагина
        """
        ...
    
    @classmethod
    def duplicate(cls, item: PluginItem) -> Any:
        """
        Создает дубликат элемента виджета.

        :param PluginItem item: Исходный элемент плагина
        :return: Дубликат элемента
        :note: В текущей реализации возвращает NotImplemented
        """
        ...
    
    @classmethod
    def createActionMenu(
            cls,
            menu: QMenu,
            widget: Any,
            item: PluginItem
    ) -> dict[str, Any]:
        """
        Создает меню действий для виджета.

        :param QMenu menu: Меню для добавления действий
        :param Any widget: Виджет плагина
        :param PluginItem item: Элемент плагина
        :return dict[str, Any]: Словарь созданных действий
        :note: Использует реализацию из родительского класса
        """
        ...