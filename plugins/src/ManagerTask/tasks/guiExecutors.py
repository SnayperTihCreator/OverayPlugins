from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QApplication, QStyle, QWidget, QFormLayout, QLineEdit, QCheckBox, QFileDialog, \
    QPushButton

from ..uis.dialogConfimCommand_ui import Ui_Info

qApp: QApplication

from PySide6.QtCore import QTimer, QElapsedTimer
from PySide6.QtWidgets import QDialog, QApplication, QStyle
from PySide6.QtGui import Qt


class DialogConfirmCommand(QDialog, Ui_Info):
    def __init__(self, timeout):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        icon = qApp.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxWarning).scaled(50, 50)
        self.label.setPixmap(icon)
        
        self.timeout = timeout
        self.remaining_time = timeout
        
        # Основной таймер для авто-принятия
        self.timer = QTimer(self, interval=timeout * 1000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.auto_accept)
        
        # Таймер для обновления отображения времени (каждую секунду)
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Для точного отслеживания времени
        self.elapsed_timer = QElapsedTimer()
        
        self.accepted.connect(self.stop_timers)
        self.rejected.connect(self.stop_timers)
    
    def setTextData(self, title, msg):
        # Добавляем информацию о таймере в сообщение
        timer_info = f"Автоматическое подтверждение через: {self.timeout} секунд"
        self.setWindowTitle(title)
        self.textBrowser.setMarkdown(msg)
        self.timeLeft.setText(timer_info)
    
    def update_countdown(self):
        # Обновляем оставшееся время
        elapsed_seconds = self.elapsed_timer.elapsed() / 1000
        self.remaining_time = max(0, self.timeout - int(elapsed_seconds))
        
        if self.remaining_time > 0:
            new_text = f"Автоматическое подтверждение через: {self.remaining_time} секунд"
        else:
            new_text = f"Подтверждение..."
        
        self.timeLeft.setText(new_text)
    
    def stop_timers(self):
        self.timer.stop()
        self.countdown_timer.stop()
    
    def auto_accept(self):
        self.stop_timers()
        self.accept()
    
    def showEvent(self, e):
        super().showEvent(e)
        self.timer.start()
        self.countdown_timer.start(1000)  # Обновление каждую секунду
        self.elapsed_timer.start()
        self.update_countdown()  # Первоначальное обновление
    
    def closeEvent(self, e):
        self.stop_timers()
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
