from typing import Optional, Any
from PySide6.QtWidgets import QWidget, QMainWindow
from API.config import Config
from API.core import APIBaseWidget
from API.PluginSetting import PluginSettingWindow


class DraggableWindow(QMainWindow, APIBaseWidget):
    """
    Перетаскиваемое окно с прозрачным фоном и возможностью настройки стилей.

    Особенности:
    - Поддерживает перетаскивание за любую область
    - Автоматически загружает конфигурацию размеров и стилей
    - Поддерживает прозрачность для ввода
    - Имеет анимацию подсветки границ для определения виджета
    - Сохраняет/восстанавливает позицию
    """
    
    def __init__(self, config: Config, parent: Optional[QWidget] = None) -> None:
        """
        Инициализирует перетаскиваемое окно.

        Args:
            config: Конфигурация окна (размеры, стили и пр.)
            parent: Родительский виджет
        """
        ...
    
    def updateData(self) -> None:
        """Обновляет внутренние данные после перезагрузки конфига."""
        ...
    
    def loadConfig(self) -> None:
        """Загружает конфигурацию размеров и стилей окна."""
        ...
    
    def reloadConfig(self) -> None:
        """Полностью перезагружает конфигурацию из файла."""
        ...
    
    def shortcut_run(self, name: str) -> None:
        """Обработчик вызова по горячей клавише."""
        ...
    
    def toggle_input(self, state: bool) -> None:
        """
        Переключает режим прозрачности для ввода.

        Args:
            state: Если True, окно становится прозрачным для ввода
        """
        ...
    
    def restoreConfig(self, config: Any) -> None:
        """
        Восстанавливает состояние окна из конфига.

        Args:
            config: Конфиг с параметрами позиции, прозрачности и др.
        """
        ...
    
    def highlightBorder(self) -> None:
        """Анимирует подсветку границ окна (визуальный фокус)."""
        ...
    
    @classmethod
    def createSettingWidget(
            cls,
            window: "DraggableWindow",
            name_plugin: str,
            parent: QWidget
    ) -> PluginSettingWindow:
        """
        Создает виджет настроек для этого окна.

        Args:
            window: Экземпляр DraggableWindow
            name_plugin: Имя плагина
            parent: Родительский виджет

        Returns:
            PluginSettingWindow: Виджет с настройками
        """
        ...