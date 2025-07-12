from enum import IntEnum, auto

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QSize
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QSlider, QStyleOptionViewItem
from PySide6.QtGui import QPalette

from .volumeController import Application, SystemVolume

__all__ = ["VolumeListModel", "VolumeItemDelegate"]


class VolumeItemRole(IntEnum):
    VOLUME = Qt.ItemDataRole.UserRole
    MUTED = auto()
    IS_SYSTEM = auto()


class VolumeListModel(QAbstractListModel):
    def __init__(self, volume_handler, parent=None):
        super().__init__(parent)
        self.volume_handler = volume_handler
        self.apps: list[Application] = []
        self.refresh()
    
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.apps)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.apps):
            return None
        
        app = self.apps[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return app.name
        elif role == VolumeItemRole.MUTED:  # ID приложения
            return app.mute
        elif role == VolumeItemRole.VOLUME:  # Volume
            return app.volume * 100
        elif role == VolumeItemRole.IS_SYSTEM:  # Muted
            return isinstance(app, SystemVolume)
        return None
    
    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or index.row() >= len(self.apps):
            return False
        
        app = self.apps[index.row()]
        
        if role == VolumeItemRole.VOLUME:  # Volume
            app.volume = value / 100
            self.dataChanged.emit(index, index, [VolumeItemRole.VOLUME])
            return True
        elif role == VolumeItemRole.MUTED:  # Muted
            app.mute = value
            self.dataChanged.emit(index, index, [VolumeItemRole.MUTED])
            return True
        
        return False
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
    
    def refresh(self):
        self.beginResetModel()
        self.apps = self.volume_handler.get_applications()
        self.endResetModel()


class VolumeItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slider_width = 150
        self.slider_height = 20
        self.item_height = 60
    
    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex):
        self.initStyleOption(option, index)
        painter.save()
        
        # Рисуем текст (название приложения)
        text_rect = option.rect.adjusted(5, 5, -self.slider_width - 10, -5)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, index.data(Qt.ItemDataRole.DisplayRole))
        
        # Рисуем слайдер громкости
        volume = index.data(VolumeItemRole.VOLUME)
        muted = index.data(VolumeItemRole.MUTED)
        
        slider_rect = option.rect.adjusted(
            option.rect.width() - self.slider_width - 5,
            (option.rect.height() - self.slider_height) // 2,
            -5,
            -(option.rect.height() - self.slider_height) // 2
        )
        
        # Рамка слайдера
        painter.setPen(option.palette.color(QPalette.ColorRole.Text))
        painter.drawRect(slider_rect)
        
        # Заливка слайдера
        fill_width = int((slider_rect.width() - 2) * volume / 100)
        fill_rect = slider_rect.adjusted(1, 1, -(slider_rect.width() - fill_width - 1), -1)
        
        if muted:
            painter.setBrush(option.palette.color(QPalette.ColorRole.Dark))
        else:
            painter.setBrush(option.palette.color(QPalette.ColorRole.Highlight))
            
            painter.drawRect(fill_rect)
            
            # Текст с процентом
            text = f"{int(volume)}% {'(Muted)' if muted else ''}"
            painter.drawText(slider_rect, Qt.AlignCenter, text)
            
            painter.restore()
    
    def sizeHint(self, option, index):
        return QSize(300, self.item_height)
    
    def createEditor(self, parent, option, index):
        slider = QSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setTickInterval(10)
        slider.setRange(0, 100)
        slider.setSingleStep(5)
        slider.setPageStep(10)
        return slider
    
    def setEditorData(self, editor, index):
        editor.setValue(int(index.data(VolumeItemRole.VOLUME)))
    
    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), VolumeItemRole.VOLUME)
    
    def updateEditorGeometry(self, editor, option, index):
        slider_rect = option.rect.adjusted(
            option.rect.width() - self.slider_width - 5,
            (option.rect.height() - self.slider_height) // 2,
            -5,
            -(option.rect.height() - self.slider_height) // 2
        )
        editor.setGeometry(slider_rect)
