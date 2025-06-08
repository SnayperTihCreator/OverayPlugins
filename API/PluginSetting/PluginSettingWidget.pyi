from PySide6.QtWidgets import QWidget
from API.core import APIBaseWidget
from .PluginSettingTemplate import PluginSettingTemplate


class PluginSettingWidget(PluginSettingTemplate):
    """
    Виджет базовых настроек для оверлейных виджетов.
    Наследует и расширяет базовый шаблон настроек плагина.

    Предоставляет:
    - Стандартный layout для элементов настроек
    - Интеграцию с системой конфигурации
    - Базовый функционал управления плагином
    """
    
    def __init__(
            self,
            obj: APIBaseWidget,
            name_plugin: str,
            parent: QWidget = None
    ) -> None:
        """
        Инициализирует виджет настроек.

        Args:
            obj: Настраиваемый виджет (наследник APIBaseWidget)
            name_plugin: Имя плагина для отображения
            parent: Родительский виджет
        """
        ...