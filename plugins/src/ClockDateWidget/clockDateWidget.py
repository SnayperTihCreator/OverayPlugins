from datetime import datetime

from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtCore import Qt, QDateTime

from API import Config, QmlDraggableWindow

from . import assets_rc


class ClockDateWidget(QmlDraggableWindow):
    
    def __init__(self, parent=None):
        super().__init__(
            Config("ClockDateWidget", "draggable_window"),
            "qrc:/clock_date_widget/ClockDateWidget.qml",
            parent)
        
        self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
        self.setRootProperty("timeFormat", self.config.clockFormat.timeFormat)
        self.setRootProperty("dateFormat", self.config.clockFormat.dateFormat)
        
        self.idTimer = self.startTimer(1000)
        
    def timerEvent(self, event, /):
        if event.id().value == self.idTimer:
            self.setRootProperty("currentDateTime", QDateTime.currentDateTime())
    
    def loadPresetData(self):
        engine = super().loadPresetData()
        
        self.setRootProperty("timeFormat", self.config.clockFormat.timeFormat)
        self.setRootProperty("dateFormat", self.config.clockFormat.dateFormat)
        
        return engine
