from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QListView, QMenu

from API import Config, DraggableWindow
from APIService import modulateIcon

from .volumeController import VolumeController
from .volumeRenderList import VolumeListModel, VolumeItemDelegate
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


class VolumeControl(DraggableWindow):
    def __init__(self, parent=None):
        self.showingList = False
        
        super().__init__(Config(__file__, "draggable_window"), parent)
        
        self.controller = VolumeController()
        
        self.box = QVBoxLayout(self.central_widget)
        self.box.setSpacing(1)
        
        header = QPushButton(modulateIcon(QIcon(":/volume_control/header.png"), QColor(self.config.theme.color)), "Volume Control")
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
    
    def act_open_volume_list(self):
        self.showingList = True
        self.loadConfig()
        self.btnOpenList.hide()
        self.btnHideList.show()
        self.controller.update()
        self.list_volume.show()
    
    def act_close_volume_list(self):
        self.showingList = False
        self.loadConfig()
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
    
    def loadConfig(self):
        super().loadConfig()
        if self.showingList:
            width, height = self.config.window.width, self.config.window.height
            self.setFixedSize(width * 2, height * 4)
    
    def hideEvent(self, event, /):
        self.controller.stop_monitoring()
        return super().hideEvent(event)
    
    def closeEvent(self, event, /):
        self.controller.close()
        return super().closeEvent(event)
    
    def showEvent(self, event, /):
        self.controller.start_monitoring(self._on_change)
        return super().showEvent(event)
