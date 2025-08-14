from datetime import datetime
import io
from json5 import dumps

from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtCore import qInfo
import psutil

from API import Config, QmlDraggableWindow

from . import assets_rc

def qprint(*args, **kwargs):
    stdout = io.StringIO()
    print(*args, **kwargs, file=stdout)
    qInfo(stdout.getvalue())


class ResourceSystem(QmlDraggableWindow):
    
    def __init__(self, parent=None):
        
        
        super().__init__(
            Config("ResourceSystem", "draggable_window"),
            "qrc:/resource_system/ResourceSystem.qml",
            parent)
        self.run_interface()
        self.idTimer = self.startTimer(1000)
        
    def timerEvent(self, event, /):
        if event.id().value == self.idTimer:
            self.run_interface()
    
    def loadPresetData(self):
        engine = super().loadPresetData()
        self.run_interface()
        return engine
    
    def run_interface(self):
        if not self.isVisible(): return
        
        self.cpu_calc()
        self.process_iter()
    
    def NetworkConnections(self):
        network_statick = psutil.net_if_stats()
        qprint(f"сетевая статистика: {dumps(network_statick, ensure_ascii=False, indent=4)}")

    def cpu_calc(self):
        total_cpu = psutil.cpu_percent(interval=1)
        speeds_cpu = psutil.cpu_freq()
        
        self.setRootProperty("total_cpu", total_cpu)
        self.setContextProperty("current_speed_cpu", speeds_cpu.current)
        self.setContextProperty("max_speed_cpu", speeds_cpu.max)
        self.setContextProperty("min_speed_cpu", speeds_cpu.min)

    def process_iter(self):
        ram_info = psutil.virtual_memory()

        mem_total = ram_info.total / 1024 / 1024 / 1024
        mem_available = ram_info.available / 1024 / 1024 / 1024
        mem_used = ram_info.used / 1024 / 1024 / 1024
        mem_percentage_usege = ram_info.percent

        self.setRootProperty("mem_total", mem_total)
        self.setContextProperty("mem_available", mem_available)
        self.setContextProperty("mem_used", mem_used)
        self.setContextProperty("mem_percentage_usege", mem_percentage_usege)
        # qprint(f"Total: {ram_info.total / 1024 / 1024 / 1024:.2f} GB")
        # qprint(f"Available: {ram_info.available / 1024 / 1024 / 1024:.2f} GB")
        # qprint(f"Used: {ram_info.used / 1024 / 1024 / 1024:.2f} GB")
        # qprint(f"Percentage usage: {ram_info.percent}%")