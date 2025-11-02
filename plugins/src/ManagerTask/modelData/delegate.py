from PySide6.QtCore import Qt, QSize, QRect, QEvent, Signal, QPoint
from PySide6.QtWidgets import QStyledItemDelegate, QApplication, QListView
from PySide6.QtGui import QPixmap, QMouseEvent, QPen, QFont, QBrush

from .core import ManagerTaskRole
from ColorControl.themeController import ThemeController

qApp: QApplication


class ManagerTaskDelegate(QStyledItemDelegate):
    customContextMenuRequested = Signal(QPoint)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.customContextMenuRequested.connect(self.parent().customContextMenuRequested.emit)
    
    def sizeHint(self, option, index):
        size: QSize = index.data(Qt.ItemDataRole.SizeHintRole)
        return QSize(self.parent().width() - 30, size.height())
    
    def createEditor(self, parent, option, index):
        return None
    
    def editorEvent(self, event, model, option, index):
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.RightButton:
                self.customContextMenuRequested.emit(event.pos())
                return True
        return super().editorEvent(event, model, option, index)
    
    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.save()
        painter.setPen(QPen(ThemeController().color("mainText"), 2))
        painter.drawRoundedRect(option.rect.adjusted(1, 0, -1, 0), 10, 10)
        painter.restore()
        painter.setPen(ThemeController().color("mainText"))
        
        painter.save()
        font: QFont = option.font
        font.setPointSizeF(font.pointSizeF() * 1.5)
        painter.setFont(font)
        idx_rect = option.rect.adjusted(10, 0, 0, 0)
        painter.drawText(idx_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str(index.row() + 1))
        painter.restore()
        
        mix_x = 70
        display_rect = option.rect.adjusted(mix_x, 5, 0, 0)
        display_text = index.data(Qt.ItemDataRole.DisplayRole)
        painter.drawText(display_rect, Qt.AlignmentFlag.AlignTop, display_text)
        
        painter.save()
        
        painter.setPen(ThemeController().color("altText"))
        extra_rect = option.rect.adjusted(mix_x, 0, 0, -5)
        extra_text = index.data(ManagerTaskRole.ExtraRole)
        painter.drawText(extra_rect, Qt.AlignmentFlag.AlignBottom, extra_text)
        
        painter.restore()
        
        status_rect = option.rect.adjusted(0, 0, -10, 0)
        status_text = index.data(ManagerTaskRole.StatusRole).upper()
        painter.drawText(status_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, status_text)
        