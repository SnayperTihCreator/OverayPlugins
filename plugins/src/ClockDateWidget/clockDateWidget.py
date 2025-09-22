from PySide6.QtCore import QDateTime

from API import Config, QmlDraggableWindow
from .config import ClockDateConfig

# noinspection PyUnresolvedReferences
from . import assets_rc


class ClockDateWidget(QmlDraggableWindow):
    
    def __init__(self, parent=None):
        super().__init__(
            Config("ClockDateWidget", "window", scheme=ClockDateConfig),
            "qrc:/clock_date_widget/ClockDateWidget.qml",
            parent)
        
        self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
        self.setRootProperty("timeFormat", self.config.data.clockFormat.timeFormat)
        self.setRootProperty("dateFormat", self.config.data.clockFormat.dateFormat)
        
    def __process__(self):
        self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
    
    def loadPresetData(self):
        engine = super().loadPresetData()
        
        self.setRootProperty("timeFormat", self.config.data.clockFormat.timeFormat)
        self.setRootProperty("dateFormat", self.config.data.clockFormat.dateFormat)
        
        return engine
