from PySide6.QtWidgets import QWidget
from .PluginSettingTemplate import PluginSettingTemplate


class PluginSettingWindow(PluginSettingTemplate):
    """
    Окно настроек плагина с дополнительными параметрами управления окном.

    Добавляет к базовым настройкам:
    - Чекбокс "Не кликабельный" (прозрачность для ввода)
    - Чекбокс "Подвижный" (возможность перемещения окна)
    """
    
    def __init__(self, obj: QWidget, name_plugin: str, parent: QWidget = None) -> None:
        """
        Инициализирует окно настроек.

        Args:
            obj: Целевой виджет/окно для настройки
            name_plugin: Имя плагина (для заголовка)
            parent: Родительское окно
        """
        ...
    
    def loader(self) -> None:
        """
        Загружает текущее состояние виджета в элементы управления.
        Определяет текущие значения:
        - Флаг прозрачности для ввода (WindowTransparentForInput)
        - Флаг возможности перемещения окна (hasMoved)
        """
        ...
    
    def send_data(self) -> dict:
        """
        Подготавливает данные настроек перед отправкой.

        Returns:
            dict: Словарь с настройками, включая:
                - hasMoved: состояние чекбокса "Подвижный"
                - noClicked: состояние чекбокса "Не кликабельный"
                + все данные из родительского класса
        """
        ...