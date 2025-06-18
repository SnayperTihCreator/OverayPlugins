from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtCore import Qt

from API import Config, OverlayWidget


class ManagerTask(OverlayWidget):
    def __init__(self, parent):
        super().__init__(Config(__file__, "overlay_widget"), parent)
    
    def reloadConfig(self):
        super().reloadConfig()
    
    def savesConfig(self):
        return super().savesConfig()
    
    def restoreConfig(self, config):
        super().restoreConfig(config)
    
    def loader(self):
        super().loader()
