from contextlib import contextmanager
from typing import Any, Dict, Iterator

from PySide6.QtCore import QSettings

from ApiPlugins.pluginItems import PluginItem
from ApiPlugins.preloader import PreLoader


class PluginControl:
    """Контроллер для управления сохранением/загрузкой конфигураций плагинов."""

    @classmethod
    def saveConfig(cls, item: PluginItem, settings: QSettings) -> None:
        """
        Сохраняет конфигурацию плагина в настройки.

        :param PluginItem item: Элемент плагина для сохранения
        :param QSettings settings: Хранилище настроек Qt
        :note: Автоматически определяет нужный загрузчик по типу плагина
        """
        ...

    @classmethod
    @contextmanager
    def enterGroup(cls, settings: QSettings, group: str) -> Iterator[None]:
        """
        Контекстный менеджер для работы с группами настроек.

        :param QSettings settings: Хранилище настроек
        :param str group: Имя группы
        """
        ...

    @staticmethod
    def getObjectWithType(objs: Dict[str, Any], type_name: str, name: str) -> Any:
        """
        Получает объект из словаря по типу и имени.

        :param objs: Словарь сгруппированных объектов
        :param type_name: Тип объекта ('Window' или 'Widget')
        :param name: Имя объекта
        :return Any: Найденный объект или None
        """
        ...

    @staticmethod
    def getDumper(type_name: str) -> PreLoader:
        """
        Возвращает загрузчик конфигурации по типу плагина.

        :param type_name: Тип плагина ('Window' или 'Widget')
        :return PreLoader: Соответствующий загрузчик
        :raises ValueError: Если тип плагина неизвестен
        """
        ...