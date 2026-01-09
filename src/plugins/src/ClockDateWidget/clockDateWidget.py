from PySide6.QtCore import QDateTime

from oapi import Config, OQMLWindow
from .config import ClockDateConfig

# noinspection PyUnresolvedReferences
from . import assets_rc


class ClockDateWidget(OQMLWindow):
    
    def __init__(self, parent=None):
        super().__init__(
            Config("ClockDateWidget", "window", scheme=ClockDateConfig),
            "qrc:/clock_date_widget/ClockDateWidget.qml",
            parent)
        
        self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
        self.setRootProperty("timeFormat", self.config.data.clock_format.time_format)
        self.setRootProperty("dateFormat", self.config.data.clock_format.date_format)
        
    def __process__(self):
        self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
    
    def loadPresetData(self):
        engine = super().loadPresetData()
        
        self.setRootProperty("timeFormat", self.config.data.clock_format.time_format)
        self.setRootProperty("dateFormat", self.config.data.clock_format.date_format)
        
        return engine
