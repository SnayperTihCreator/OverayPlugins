import uuid

from PySide6.QtWidgets import QDialog, QListWidgetItem

from . import tasks
from .uis.dialogCreateTask_ui import Ui_dialogCreateTask
from .dialogCreateAction import CreateDialogAction


class CreateDialogTask(QDialog, Ui_dialogCreateTask):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnCreateAction.pressed.connect(self.actCreateAction)
        self._actions = []
    
    def actCreateAction(self):
        dialog = CreateDialogAction(self)
        if dialog.exec():
            action = dialog.getItem()
            self.add_action(action)
    
    def add_action(self, action):
        self._actions.append(action)
        item = QListWidgetItem(
            f"{action.executor.display_name}: {action.executor.description} - {action.trigger.description}")
        self.listActions.addItem(item)
    
    def getItem(self):
        return tasks.Task(self.nameLineEdit.text(), uuid.uuid4().hex[:5], self._actions)
