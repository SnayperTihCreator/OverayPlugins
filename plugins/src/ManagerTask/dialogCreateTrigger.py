from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt

from .uis.dialogCreateTrigger_ui import Ui_dialogCreateTrigger
from .tasks.triggers import *
from .tasks import BaseTrigger

triggers = [AbsoluteDateTimeTrigger, RelativeDateTimeTrigger]


class CreateDialogTrigger(QDialog, Ui_dialogCreateTrigger):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.whatCallComboBox.currentIndexChanged.connect(self.actChoseTrig)
        for trig in triggers:
            self.whatCallComboBox.addItem(trig.display_name, userData=trig)
        
        self.trigMenu: Optional[QWidget] = None
        self.trigCallback = None
    
    def actChoseTrig(self, idx):
        if idx > 0:
            trig = self.whatCallComboBox.itemData(idx, Qt.ItemDataRole.UserRole)
            newTrigMenu, newTrigCallback = trig.getGUI()
            if self.trigMenu is None:
                self.trigMenu, self.trigCallback = newTrigMenu, newTrigCallback
                self.formLayout.replaceWidget(self.frameTriggers, self.trigMenu)
                self.frameTriggers.hide()
            else:
                self.formLayout.replaceWidget(self.trigMenu, newTrigMenu)
                self.trigMenu.deleteLater()
                self.trigMenu, self.trigCallback = newTrigMenu, newTrigCallback
        elif self.trigMenu is not None:
            self.formLayout.replaceWidget(self.trigMenu, self.frameTriggers)
            self.trigMenu.hide()
            self.frameTriggers.show()
            self.trigMenu = None
            self.trigCallback = None
            
    def getItem(self):
        return self.trigCallback()