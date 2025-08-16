from typing import Optional, Any

from PySide6.QtQuick import QQuickItem
from PySide6.QtWidgets import QWidget, QMainWindow
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlEngine

from API.config import Config
from Common.core import APIBaseWidget
from API.PluginSetting import PluginSettingWindow


class DraggableWindow(QMainWindow, APIBaseWidget):
    central_widget: QWidget
    config: Config
    reloading: bool
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

        :param Config config: Конфигурация окна (размеры, стили и пр.)
        :param Optional[QWidget] parent: Родительский виджет
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
        """
        Обработчик вызова по горячей функции.

        :param str name: Имя действия
        """
        ...
    
    def toggle_input(self, state: bool) -> None:
        """
        Переключает режим прозрачности для ввода.

        :param bool state: Если True, окно становится прозрачным для ввода.
        :note: Не влияет на визуальную прозрачность, только на обработку событий
        """
        ...
    
    def restoreConfig(self, config: Any) -> None:
        """
        Восстанавливает состояние окна из конфига.

        :param Any config: Конфиг с параметрами позиции, прозрачности и др.
        """
        ...
    
    def highlightBorder(self) -> None:
        """
        Анимирует подсветку границ окна (визуальный фокус).

        :note: Использует анимацию длительностью 300 мс
        """
    
    @classmethod
    def createSettingWidget(
            cls,
            window: "DraggableWindow",
            name_plugin: str,
            parent: QWidget
    ) -> PluginSettingWindow:
        """
        Создает виджет настроек для этого окна.

        :param DraggableWindow window: Экземпляр DraggableWindow
        :param str name_plugin: Имя плагина
        :param QWidget parent: Родительский виджет
        :return PluginSettingWindow: Виджет с настройками
        """
    
    def savesConfig(self) -> dict[str, Any]:
        """
        Возвращает словарь для сохранения параметров в глобальное сохранение

        :return: Словарь с конфигурационными параметрами
        :rtype: dict[str, Any]
        :note: Содержит позицию, прозрачность ввода и перетаскивания
        """
    
    
class QmlDraggableWindow(DraggableWindow):
    """
    Перетаскиваемое окно с QML-сценой.

    Наследует функциональность DraggableWindow и добавляет QML-интеграцию.
    """
    
    central_widget: QQuickWidget
    
    def __init__(self, config: Config, url: str, parent: Optional[QWidget] = None):
        """
        Инициализирует QML-окно.

        :param Config config: Конфигурация окна
        :param str url: Путь к QML-файлу интерфейса
        :param Optional[QWidget] parent: Родительский виджет
        """
    
    def loadQmlContent(self, url: str):
        """
        Загружает QML-файл.

        :param str url: Путь к QML-файлу
        :raises QMLException: Если загрузка не удалась
        """
    
    def getRootQml(self) -> QQuickItem:
        """
        Возвращает корневой элемент загруженной QML-сцены.

        :return QQuickItem: Корневой QML-элемент
        """
    
    def setRootProperty(self, name:str, value: Any):
        """
        Устанавливает свойство корневого QML-объекта.
        
        :param str name: Имя свойства для установки
        :param Any value: Значение свойства
        """
    
    def setContextProperty(self, name: str, value: Any):
        """
        Регистрирует глобальную переменную в QML-контексте.

        :param str name: Имя переменной для доступа из QML.
        :param Any value: Значение переменной.
        """
    
    def loadPresetData(self)->QQmlEngine:
        """
        Загружает предустановленные данные в QML-движок и возвращает экземпляр движка.
        
        :return QQmlEngine: Экземпляр QML-движка после загрузки данных.
        """