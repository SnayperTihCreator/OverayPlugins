from abc import ABC, abstractmethod
from typing import Any, Dict

from PySide6.QtGui import QColor, QFont, QIcon, QPixmap, QImage
from functools import wraps


def stripColor(func: Any) -> Any:
    """
    Декоратор для преобразования QColor в hex-строку (без #).

    :param func: Декорируемая функция
    :return: Функция-обертка
    :note: Преобразует только возвращаемые значения типа QColor
    """
    ...


class Theme(ABC):
    """
    Абстрактный базовый класс для цветовых тем приложения.

    Обеспечивает:
    - Базовые цвета интерфейса
    - Управление шрифтами
    - Тонирование изображений
    - Работу с иконками
    """
    
    font: QFont
    """Основной шрифт темы"""
    
    baseColor: QColor
    """Базовый цвет темы"""
    
    mainTextColor: QColor
    """Основной цвет текста"""
    
    altTextColor: QColor
    """Альтернативный цвет текста"""
    
    @property
    def base(self) -> str:
        """Базовый цвет в hex-формате (без #)"""
        ...
    
    @property
    def mainText(self) -> str:
        """Цвет основного текста в hex-формате (без #)"""
        ...
    
    @property
    def altText(self) -> str:
        """Цвет альтернативного текста в hex-формате (без #)"""
        ...
    
    def disabledText(self) -> str:
        """
        Цвет неактивного текста.

        :return: Hex-строка (без #)
        """
        ...
    
    def baseInput(self) -> str:
        """
        Цвет фона input-элементов.

        :return: Hex-строка (без #)
        """
        ...
    
    def hovered(self) -> str:
        """
        Цвет в состоянии hover.

        :return: Hex-строка (без #)
        """
        ...
    
    def pressed(self) -> str:
        """
        Цвет в состоянии pressed.

        :return: Hex-строка (без #)
        """
        ...
    
    def mainSelectText(self) -> str:
        """
        Цвет выделенного текста.

        :return: Hex-строка (без #)
        """
        ...
    
    def modulateImage(self) -> QColor:
        """
        Возвращает цвет для тонирования изображений.

        :return: Цвет тонирования
        """
        ...
    
    def getModulateImageQt(self, path: str, typeImage: str = "pixmap") -> Any:
        """
        Тонирует изображение из ресурсов Qt.

        :param path: Путь к ресурсу
        :param typeImage: Тип изображения (pixmap/icon/image)
        :return: Тонированное изображение
        :raises ValueError: Если тип изображения неизвестен
        """
        ...
    
    def getModulateImage(self, path: str, typeImage: str = "pixmap") -> Any:
        """
        Тонирует изображение из файла.

        :param path: Путь к файлу
        :param typeImage: Тип изображения (pixmap/icon/image)
        :return: Тонированное изображение
        :raises ValueError: Если тип изображения неизвестен
        """
        ...
    
    def modulated(self, obj: Any) -> Any:
        """
        Тонирует изображение/иконку в зависимости от типа.

        :param obj: Объект для тонирования (QIcon/QPixmap/QImage)
        :return: Тонированный объект
        :raises TypeError: Если тип объекта не поддерживается
        """
        ...
    
    @staticmethod
    def addFontFile(path: str) -> None:
        """
        Добавляет шрифт в базу приложения.

        :param path: Путь к файлу шрифта
        """
        ...
    
    def addImagePath(self, name: str, path: str) -> None:
        """
        Регистрирует путь к изображению.

        :param name: Имя изображения
        :param path: Путь к файлу
        """
        ...
    
    def getImage(self, name: str) -> str:
        """
        Возвращает путь к изображению по имени.

        :param name: Имя изображения
        :return: Путь к файлу
        :raises KeyError: Если имя не найдено
        """
        ...
    
    @abstractmethod
    def preInitTheme(self, *args: Any) -> None:
        """
        Вызывается перед инициализацией темы.

        :param args: Дополнительные параметры
        """
        ...
    
    @abstractmethod
    def postInitTheme(self, *args: Any) -> None:
        """
        Вызывается после инициализации темы.

        :param args: Дополнительные параметры
        """
        ...


__all__ = ["Theme", "stripColor"]