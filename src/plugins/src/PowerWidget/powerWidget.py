from PySide6.QtCore import QTimer
import psutil

from oapi import Config, OQMLWindow
from .config import PowerWidgetConfig
# noinspection PyUnresolvedReferences
from . import assets_rc


class PowerWidget(OQMLWindow):
    def __init__(self, parent=None):
        super().__init__(
            Config("PowerWidget", "window", scheme=PowerWidgetConfig),
            "qrc:/power_widget/PowerWidget.qml",
            parent)
        
        self._last_percent = 0
        self._last_left_time = ""
    
    def __process__(self):
        super().__process__()
        battery = psutil.sensors_battery()
        if battery is None:
            return
        
        percent = battery.percent
        if percent != self._last_percent or self.reloading:
            self._last_percent = percent
            self.setRootProperty("powerLevel", percent)
        
        time_left = self._calculate_time_left(battery)
        
        if time_left != self._last_left_time or self.reloading:
            self._last_left_time = time_left
            self.setRootProperty("timeLeft", time_left)
            self.setRootProperty("charging", battery.power_plugged)
    
    def _calculate_time_left(self, battery):
        if battery.power_plugged:
            return "Заряжается"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            return "Рассчитывается"
        elif (battery.secsleft // 3600) > 100_000:
            return "Рассчитывается"
        else:
            return f"{battery.secsleft // 3600} ч {(battery.secsleft % 3600) // 60} мин"
