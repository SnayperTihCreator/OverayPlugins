from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView

from .tasks import Action

from .uis.dialogActions_ui import Ui_dialogAction


class DialogAction(QDialog, Ui_dialogAction):
    def __init__(self, actions: list[Action], parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.actions = []
        
        for action in actions:
            self.add_action(action)
    
    def add_action(self, action: Action):
        idx = self.tableWidget.rowCount()
        self.tableWidget.insertRow(idx)
        
        itemExecutor = QTableWidgetItem(action.executor.description)
        self.tableWidget.setItem(idx, 0, itemExecutor)
        itemStatus = QTableWidgetItem(action.status.name)
        self.tableWidget.setItem(idx, 1, itemStatus)
        itemTrigger = QTableWidgetItem(action.trigger.description)
        self.tableWidget.setItem(idx, 2, itemTrigger)
        
        self.actions.append(action)
