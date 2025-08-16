from types import ModuleType
from typing import Any, Dict

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMenu

from .preloader import PreLoader
from ApiPlugins.pluginItems import PluginItem


class WindowPreLoader(PreLoader):
    """Загрузчик оконных плагинов с поддержкой дублирования."""
    
    @classmethod
    def overCreateItem(
            cls,
            module: ModuleType,
            checked: bool = False,
            count_dup: int = 0,
            is_dup: bool = False
    ) -> PluginItem:
        """
        Создает элемент окна с настройками дублирования.

        :param module: Модуль плагина
        :param checked: Флаг активности
        :param count_dup: Счетчик дубликатов
        :param is_dup: Флаг дублирования
        :return PluginItem: Созданный элемент плагина
        """
        ...
    
    @classmethod
    def overRunFunction(cls, module: ModuleType, parent: Any) -> Any:
        """
        Создает окно плагина через module.createWindow().
        
        :return: Созданное окно
        """
        ...
    
    @classmethod
    def overSaved(cls, item: PluginItem, setting: QSettings) -> None:
        """
        Сохраняет параметры дублирования в настройки.
        
        :param item: Элемент плагина
        :param setting: Хранилище настроек
        """
        ...
    
    @classmethod
    def overLoaded(cls, setting: QSettings, name: str, parent: Any) -> None:
        """
        Заглушка для дополнительной загрузки.
        
        """
        ...
    
    @classmethod
    def getParameterCreateItem(
            cls,
            setting: QSettings,
            name: str,
            parent: Any
    ) -> tuple[int, bool]:
        """
        Получает параметры дублирования из настроек.
        
        :return: (count_dub, is_dub)
        """
        ...
    
    @classmethod
    def activatedWidget(cls, state: bool, target: Any) -> None:
        """
        Управляет видимостью окна.
        :param state: Если True - показывает окно
        """
        ...
    
    @classmethod
    def duplicate(cls, item: PluginItem) -> PluginItem:
        """
        Создает дубликат окна.
        :return PluginItem: Новый экземпляр PluginItem
        """
        ...
    
    @classmethod
    def createActionMenu(
            cls,
            menu: QMenu,
            widget: Any,
            item: PluginItem
    ) -> Dict[str, Any]:
        """
        Создает меню с доп. действиями для окон:
        - Highlight Border
        - Duplicate
        - Delete duplicate (если isDuplication)

        :return: Словарь QAction'ов
        """