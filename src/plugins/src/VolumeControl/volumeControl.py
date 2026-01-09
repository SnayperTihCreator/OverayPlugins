from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QListView, QMenu

from oapi import Config, OWindow, CLInterface, ThemeController

from .volumeController import VolumeController
from .volumeRenderList import VolumeListModel, VolumeItemDelegate
# noinspection PyUnresolvedReferences
from . import icons_rc


class CustomListView(QListView):
    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.parent().mousePressEvent(event)
            return
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.parent().mouseMoveEvent(event)
            return
        return super().mouseMoveEvent(event)


class VolumeControl(OWindow, CLInterface):
    @CLInterface.register()
    def action_set_master_volume(self, volume: str):
        self.controller.set_system_volume(float(volume))
        return True
    
    def __init__(self, parent=None):
        self.showingList = False
        
        super().__init__(Config("VolumeControl", "window"), parent)
        
        self.controller = VolumeController()
        
        self.box = QVBoxLayout(self.central_widget)
        self.box.setSpacing(1)
        
        header = QPushButton("Volume Control")
        ThemeController().registerWidget(header, ":/volume_control/header.png", "setIcon", "icon", True)
        ThemeController().updateWidget(header)
        header.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        header.setIconSize(QSize(20, 20))
        
        self.btnUpdate = QPushButton("Update")
        self.btnOpenList = QPushButton("Open List")
        self.btnHideList = QPushButton("Hide List")
        
        self.modelVolumeList = VolumeListModel(self.controller, self)
        self.volumeItemDegeta = VolumeItemDelegate(self)
        self.list_volume = CustomListView(self)
        self.list_volume.setModel(self.modelVolumeList)
        self.list_volume.setItemDelegate(self.volumeItemDegeta)
        self.list_volume.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_volume.customContextMenuRequested.connect(self.contextMenuOpen)
        self.list_volume.setIconSize(QSize(64, 64))
        
        self.btnUpdate.pressed.connect(self.modelVolumeList.refresh)
        self.btnOpenList.pressed.connect(self.act_open_volume_list)
        self.btnHideList.pressed.connect(self.act_close_volume_list)
        
        self.box.addWidget(header)
        
        self.box.addWidget(self.list_volume)
        self.list_volume.hide()
        
        self.box.addWidget(self.btnHideList)
        self.btnHideList.hide()
        
        self.box.addWidget(self.btnOpenList)
        self.box.addWidget(self.btnUpdate)
        
        self.time_msec = 5000
    
    def __process__(self):
        self.modelVolumeList.refresh()
    
    def act_open_volume_list(self):
        self.showingList = True
        self.load_config()
        self.btnOpenList.hide()
        self.btnHideList.show()
        self.controller.update()
        self.list_volume.show()
    
    def act_close_volume_list(self):
        self.showingList = False
        self.load_config()
        self.btnOpenList.show()
        self.btnHideList.hide()
        self.list_volume.hide()
    
    def contextMenuOpen(self, pos):
        idx = self.list_volume.indexAt(pos)
        app = self.modelVolumeList.getApplication(idx)
        
        menu = QMenu()
        
        actChangeMute = menu.addAction("Change muted")
        
        action = menu.exec(self.list_volume.mapToGlobal(pos))
        
        if action == actChangeMute:
            app.mute = not app.mute
    
    def _on_change(self, *args):
        self.modelVolumeList.on_change_value(*args)
        
    def load_config(self):
        super().load_config()
        if self.showingList:
            width, height = self.config.data.window.width, self.config.data.window.height
            self.setFixedSize(width * 2.5, height * 4)
    
    def hideEvent(self, event, /):
        self.controller.stop_monitoring()
        return super().hideEvent(event)
    
    def closeEvent(self, event, /):
        self.controller.close()
        return super().closeEvent(event)
    
    def showEvent(self, event, /):
        self.controller.start_monitoring(self._on_change)
        return super().showEvent(event)
    
    def save_status(self):
        ldt = super().save_status()
        ldt.set("openList", self.showingList)
        return ldt
    
    def load_status(self, status):
        super().load_status(status)
        if status.get("openList", False):
            self.act_open_volume_list()
        else:
            self.act_close_volume_list()
