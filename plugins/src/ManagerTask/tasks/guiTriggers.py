from datetime import timedelta, time

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QWidget, QFormLayout, QDateTimeEdit, QTimeEdit


class WidgetAbsoluteDateTimeTrigger(QWidget):
    def __init__(self):
        super().__init__()
        box = QFormLayout(self)
        
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        
        box.addRow("Время пуска", self.dateTimeEdit)
    
    def callback(self, trigger):
        return trigger(self.dateTimeEdit.dateTime().toPython().replace(microsecond=0))


class WidgetRelativeDateTimeTrigger(QWidget):
    def __init__(self):
        super().__init__()
        box = QFormLayout(self)
        
        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        
        box.addRow("Через сколько запустить:", self.timeEdit)
    
    def callback(self, trigger):
        time_: time = self.timeEdit.time().toPython()
        return trigger(timedelta(hours=time_.hour, minutes=time_.minute, seconds=time_.second))


__all__ = ["WidgetAbsoluteDateTimeTrigger", "WidgetRelativeDateTimeTrigger"]
