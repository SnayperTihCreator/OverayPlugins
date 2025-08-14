from enum import IntEnum, auto

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QSize, QPoint, QRect
from PySide6.QtWidgets import QStyledItemDelegate, QSlider, QStyleOptionViewItem, QLabel
from PySide6.QtGui import QPalette, QIcon

from ColorControl.themeController import ThemeController

from .volumeController import Application, SystemVolume, BaseVolumeHandler

__all__ = ["VolumeListModel", "VolumeItemDelegate"]


class VolumeItemRole(IntEnum):
    VOLUME = Qt.ItemDataRole.UserRole
    MUTED = auto()
    IS_SYSTEM = auto()
    CONTROLLER = auto()


class VolumeListModel(QAbstractListModel):
    def __init__(self, volume_handler, parent=None):
        super().__init__(parent)
        self.volume_handler: BaseVolumeHandler = volume_handler
        self.apps: list[Application] = []
        self.refresh()
        # self.volume_handler.start_monitoring(self._on_change_value)
    
    def on_change_value(self, volume: Application, params):
        try:
            idx = self.apps.index(volume)
            index = self.createIndex(idx, 0)
            self.dataChanged.emit(index, index, [VolumeItemRole.VOLUME, VolumeItemRole.MUTED])
        except IndexError:
            pass
    
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
        elif role == VolumeItemRole.CONTROLLER:
            return app
        elif role == Qt.ItemDataRole.DecorationRole:
            return QIcon(app.icon_path) if app.icon_path is not None else QIcon()
        return None
    
    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or index.row() >= len(self.apps):
            return False
        
        app = self.apps[index.row()]
        
        if role == VolumeItemRole.VOLUME:  # Volume
            self.volume_handler.set_application_volume(app.pid, value / 100)
            self.dataChanged.emit(index, index, [VolumeItemRole.VOLUME])
            return True
        elif role == VolumeItemRole.MUTED:  # Muted
            self.volume_handler.set_application_mute(app.pid, value)
            self.dataChanged.emit(index, index, [VolumeItemRole.MUTED])
            return True
        
        return False
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
    
    def refresh(self):
        self.beginResetModel()
        self.volume_handler.update()
        self.apps = self.volume_handler.get_applications()
        self.endResetModel()
    
    def getApplication(self, index: QModelIndex) -> Application:
        return self.data(index, VolumeItemRole.CONTROLLER)


class SliderPopup(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(0, 0, 0, 180); color: white; border-radius: 4px; padding: 2px 6px;")
        self.hide()


class VolumeItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slider_width = 150
        self.slider_height = 20
        self.item_height = 60
        self.spacing = 5
        self.popup_slider = SliderPopup()
        self.closeEditor.connect(lambda *args: self.popup_slider.hide())
    
    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex):
        self.initStyleOption(option, index)
        painter.save()
        
        volume = index.data(VolumeItemRole.VOLUME)
        muted = index.data(VolumeItemRole.MUTED)
        icon = index.data(Qt.ItemDataRole.DecorationRole)  # Получаем иконку
        app_name = index.data(Qt.ItemDataRole.DisplayRole)  # Получаем название
        
        # Область для иконки/названия
        content_rect = option.rect.adjusted(5, 5, -self.slider_width - 10, -5)
        icon_size = option.widget.iconSize()
        
        # Рисуем иконку если есть
        current_x = content_rect.left()
        if icon and not icon.isNull():
            
            icon_rect = QRect(QPoint(current_x, content_rect.top()), icon_size)
            
            icon = ThemeController().modulated(icon)
            icon.paint(painter, icon_rect)
            current_x += icon_size.width() + self.spacing
        
        # Всегда рисуем текст
        text_rect = QRect(current_x, content_rect.top(),
                          content_rect.right() - current_x, content_rect.height())
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, app_name)
        
        # Устанавливаем всплывающую подсказку с названием
        if option.widget:
            option.widget.setToolTip(app_name)
        
        # Рисуем слайдер громкости (остальной код без изменений)
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
        
        slider.valueChanged.connect(lambda value: self.show_popup_slider(value, slider))
        slider.sliderPressed.connect(self.popup_slider.show)
        slider.sliderReleased.connect(self.popup_slider.hide)
        return slider
    
    def show_popup_slider(self, value: int, slider: QSlider):
        self.popup_slider.setText(str(value))
        
        # Позиционируем popup над ползунком
        slider_pos = slider.mapToGlobal(QPoint(0, 0))
        handle_x = int((slider.value() / slider.maximum()) * slider.width())
        
        self.popup_slider.move(
            slider_pos.x() + handle_x - 10,
            slider_pos.y() - slider.height()
        )
        self.popup_slider.show()
    
    def setEditorData(self, editor, index):
        editor.setValue(int(index.data(VolumeItemRole.VOLUME)))
        self.popup_slider.setText(str(editor.value()))
    
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
