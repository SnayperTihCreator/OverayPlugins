from PySide6.QtGui import QColor, QFont
from ColorControl.theme import Theme


class DefaultTheme(Theme):
    """
    Стандартная цветовая тема приложения.

    Наследует базовые параметры темы и добавляет:
    - Основные цвета интерфейса
    - Настройки шрифтов
    """
    
    baseColor: QColor = ...
    """Базовый цвет фона"""
    
    mainTextColor: QColor = ...
    """Основной цвет текста"""
    
    altTextColor: QColor = ...
    """Альтернативный цвет текста"""
    
    font: QFont = ...
    """Основной шрифт (Montserrat, 12pt, Bold)"""
    
    def preInitTheme(self, *args: Any) -> None:
        """
        Выполняется перед инициализацией темы.

        :param args: Дополнительные аргументы
        :note: В текущей реализации не выполняет действий
        """
        ...
    
    def postInitTheme(self, *args: Any) -> None:
        """
        Выполняется после инициализации темы.

        :param args: Дополнительные аргументы
        :note: В текущей реализации не выполняет действий
        """
        ...