from PySide6.QtWidgets import QDialog

from .tasks import Action

from .uis.dialogActions_ui import Ui_dialogAction
from .modelData import ManagerTaskDelegate, ModelAction


class DialogAction(QDialog, Ui_dialogAction):
    def __init__(self, actions: list[Action], parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self._modelAction = ModelAction()
        self._delegate = ManagerTaskDelegate(self.listView)
        self.listView.setItemDelegate(self._delegate)
        self.listView.setModel(self._modelAction)
        
        for action in actions:
            self._modelAction.addAction(action)
