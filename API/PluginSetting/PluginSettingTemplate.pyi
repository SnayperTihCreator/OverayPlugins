from typing import TypeAliasType
from PySide6.QtWidgets import QWidget
from API.core import APIBaseWidget


OverlayWidget = TypeAliasType("OverlayWidget")
Ui_Form = TypeAliasType("Ui_Form")


class PluginSettingTemplate(OverlayWidget, Ui_Form):
    """
    Базовый шаблон окна настроек плагина.

    Предоставляет общий функционал для всех окон настроек:
    - Отображение имени плагина
    - Кнопка открытия папки плагина
    - Управление позицией окна (X/Y координаты)
    - Стандартные кнопки OK/Cancel
    """
    
    def __init__(self, obj: APIBaseWidget, name_plugin: str, parent: QWidget = None) -> None:
        """
        Инициализирует шаблон настроек плагина.

        Args:
            obj: Целевой виджет/окно для настройки
            name_plugin: Имя плагина (отображается в заголовке)
            parent: Родительское окно
        """
        ...
    
    def openFolderPlugin(self) -> None:
        """Открывает проводник в папке с плагином."""
        ...
    
    def confirming(self) -> None:
        """Обработчик подтверждения настроек - применяет изменения к целевому виджету."""
        ...
    
    def canceling(self) -> None:
        """Обработчик отмены настроек - восстанавливает предыдущие значения."""
        ...
    
    def loader(self) -> None:
        """
        Загружает текущее состояние целевого виджета в элементы управления.
        Включает текущие координаты положения окна.
        """
        ...
    
    def send_data(self) -> dict:
        """
        Формирует данные настроек для отправки.

        Returns:
            dict: Словарь с настройками, включая:
                - position: текущие координаты окна (QPoint)
        """
        ...