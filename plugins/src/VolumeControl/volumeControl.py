from PySide6.QtWidgets import QVBoxLayout, QPushButton, QListView

from API import Config, DraggableWindow

from .volumeController import VolumeController
from .volumeRenderList import VolumeListModel, VolumeItemDelegate


class CustomListView(QListView):
    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            event.ignore()  # Пропускаем событие родителю
            return
        super().mousePressEvent(event)

class VolumeControl(DraggableWindow):
    def __init__(self, parent=None):
        self.showingList = False
        
        super().__init__(Config(__file__, "draggable_window"), parent)
        
        self.controller = VolumeController()
        
        self.box = QVBoxLayout(self.central_widget)
        self.box.setSpacing(1)
        
        self.btnUpdate = QPushButton("Update")
        self.btnOpenList = QPushButton("Open List")
        self.btnHideList = QPushButton("Hide List")
        
        self.modelVolumeList = VolumeListModel(self.controller, self)
        self.volumeItemDegeta = VolumeItemDelegate(self)
        self.list_volume = CustomListView(self)
        self.list_volume.setModel(self.modelVolumeList)
        self.list_volume.setItemDelegate(self.volumeItemDegeta)
        
        self.btnUpdate.pressed.connect(self.controller.update)
        self.btnOpenList.pressed.connect(self.act_open_volume_list)
        self.btnHideList.pressed.connect(self.act_close_volume_list)
        
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
        
    def showEvent(self, event, /):
        self.controller.start_monitoring(self._on_volume_event)
        return super().showEvent(event)
    
    def loadConfig(self):
        super().loadConfig()
        if self.showingList:
            width, height = self.config.window.width, self.config.window.height
            self.setFixedSize(width*2, height*4)
    
    def _on_volume_event(self, *args):
        print(args)
    
    def hideEvent(self, event, /):
        self.controller.stop_monitoring()
        return super().hideEvent(event)
        
    def closeEvent(self, event, /):
        self.controller.close()
        return super().closeEvent(event)