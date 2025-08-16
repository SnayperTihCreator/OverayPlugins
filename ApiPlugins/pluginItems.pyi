from enum import IntEnum, auto
from types import ModuleType
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from Common.core import APIBaseWidget


class PluginItemRole(IntEnum):
    """
    Роли данных для элементов плагина.

    Используются для идентификации типов данных в моделях Qt.
    """
    TypePluginRole = Qt.ItemDataRole.UserRole  #: Роль типа плагина
    ActiveRole = auto()  #: Роль активности плагина
    Self = auto()  #: Роль доступа к самому объекту
    Icon = auto()  #: Роль иконки плагина
    Duplication = auto()  #: Роль флага дублирования


class PluginItem:
    """
    Класс-контейнер для информации о плагине.

    Содержит все необходимые данные и методы для работы с плагином.
    """
    
    def __init__(self, module: ModuleType, typeModule: str, active: bool = False) -> None:
        """
        Инициализирует элемент плагина.

        :param ModuleType module: Модуль плагина
        :param str typeModule: Тип модуля ("Window" или "Widget")
        :param bool active: Флаг активности плагина
        """
    
    @property
    def save_name(self) -> str:
        """
        Генерирует уникальное имя для сохранения.

        :return str: Имя в формате "имяплагина_типмодуля"
        """
    
    @property
    def icon(self) -> str:
        """
        Получает путь к иконке плагина.

        :return str: Путь к иконке из темы.
        :note: Ищет иконку по пути plugin://имя_модуля/icon.png
        """
    
    def clone(self) -> 'PluginItem':
        """
        Создает клон элемента плагина.

        :return PluginItem: Новый экземпляр PluginItem
        """
    
    def updateStateItem(self, state: bool) -> None:
        """
        Обновляет состояние активности плагина.

        :param bool state: Новое состояние активности
        """
    
    def build(self, parent: QWidget) -> Union[APIBaseWidget, QWidget]:
        """
        Создает виджет плагина.

        :param QWidget parent: Родительский виджет
        :return Union[APIBaseWidget, QWidget]: Созданный виджет
        """