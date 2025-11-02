from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt

from .uis.dialogCreateAction_ui import Ui_dialogCreateAction
from .tasks import Action, AndTrigger, BaseTrigger
from .tasks.executors import *
from .dialogCreateTrigger import CreateDialogTrigger

executors = [RunCommandExecutor, RunAppExecutor]


class CreateDialogAction(QDialog, Ui_dialogCreateAction):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.frameActions.hide()
        self.whatCallComboBox.currentIndexChanged.connect(self.actChoseExecutor)
        self.btnCreateTrigger.pressed.connect(self.actCreateTrigger)
        for exec_ in executors:
            self.whatCallComboBox.addItem(exec_.display_name, userData=exec_)
        self.executorMenu: Optional[QWidget] = None
        self.executorCallback = None
        
        self.globalTriggers = AndTrigger()
    
    def actChoseExecutor(self, idx):
        if idx > 0:
            execs = self.whatCallComboBox.itemData(idx, Qt.ItemDataRole.UserRole)
            newExecMenu, newExecCallback = execs.getGUI()
            if self.executorMenu is None:
                self.executorMenu, self.executorCallback = newExecMenu, newExecCallback
                self.formLayout.replaceWidget(self.frameActions, self.executorMenu)
                self.frameActions.hide()
            else:
                self.formLayout.replaceWidget(self.executorMenu, newExecMenu)
                self.executorMenu.deleteLater()
                self.executorMenu, self.executorCallback = newExecMenu, newExecCallback
        elif self.executorMenu is not None:
            self.formLayout.replaceWidget(self.executorMenu, self.frameActions)
            self.frameActions.show()
            self.executorMenu.hide()
            self.executorMenu = None
            self.executorCallback = None
    
    def actCreateTrigger(self):
        dialog = CreateDialogTrigger(self)
        if dialog.exec():
            trig = dialog.getItem()
            self.add_trig(trig)
            
    def add_trig(self, trig: BaseTrigger):
        self.globalTriggers.add(trig)
        item = QListWidgetItem(f"{trig.display_name}: {trig.description}")
        self.listTriggers.addItem(item)
    
    def getItem(self):
        return Action(self.executorCallback(), self.globalTriggers)
