from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QApplication, QStyle, QWidget, QFormLayout, QLineEdit, QCheckBox, QFileDialog, \
    QPushButton

from ..uis.dialogConfimCommand_ui import Ui_Info

qApp: QApplication


class DialogConfirmCommand(QDialog, Ui_Info):
    def __init__(self, timeout):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()|Qt.WindowType.WindowStaysOnTopHint)
        icon = qApp.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxWarning).scaled(50, 50)
        self.label.setPixmap(icon)
        
        self.timer = QTimer(self, interval=timeout*1000)
        
        self.accepted.connect(self.timer.stop)
        self.rejected.connect(self.timer.stop)
        
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.auto_accept)
    
    def setTextData(self, title, msg):
        self.setWindowTitle(title)
        self.textBrowser.setMarkdown(msg)
        
    def auto_accept(self):
        self.accept()
        
    def showEvent(self, e):
        super().showEvent(e)
        self.timer.start()
        
    def closeEvent(self, e):
        self.timer.stop()
        super().closeEvent(e)


class WidgetRunCommandExecutor(QWidget):
    def __init__(self):
        super().__init__()
        box = QFormLayout(self)
        
        self.lineEdit = QLineEdit()
        self.checkBox = QCheckBox()
        box.addRow("Команда", self.lineEdit)
        box.addRow("Подтверждение", self.checkBox)
    
    def callback(self, executor):
        return executor(self.lineEdit.text(), self.checkBox.isChecked())


class WidgetRunAppExecutor(QWidget):
    def __init__(self):
        super().__init__()
        box = QFormLayout(self)

        self.runAppPath = QLineEdit()
        btnChoiceApp = QPushButton("Choice app")
        btnChoiceApp.pressed.connect(self.actSetPathApp)
        self.argsLineEdit = QLineEdit()
        self.checkBox = QCheckBox()
        
        box.addRow("Файл", self.runAppPath)
        box.addRow(btnChoiceApp)
        box.addRow("Параметры", self.argsLineEdit)
        # box.addRow("Подтверждение", self.checkBox)
    
    def actSetPathApp(self):
        pathApp, _ = QFileDialog.getOpenFileName(self, "Выберете исполняемый файл", "",
                                                 "Исполняемые файлы (*.exe *.bat *.sh);;Все файлы (*)")
        self.runAppPath.setText(pathApp)
        
    def callback(self, executor):
        return executor(Path(self.runAppPath.text()), self.argsLineEdit.text())
    
    
__all__ = ["DialogConfirmCommand", "WidgetRunCommandExecutor", "WidgetRunAppExecutor"]