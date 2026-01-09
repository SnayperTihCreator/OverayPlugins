from functools import partial

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QSize

from ..tasks import Action, ActionStatus
from .core import ManagerTaskRole


class ModelAction(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._actions: list[Action] = []
    
    def addAction(self, action: Action):
        if not isinstance(action, Action):
            raise TypeError
        self.beginInsertRows(QModelIndex(), len(self._actions), len(self._actions))
        self._actions.append(action)
        action.status_changed.connect(partial(self._on_handled_update_status, action))
        self.endInsertRows()
    
    def _on_handled_update_status(self, task, _status):
        row = self._actions.index(task)
        idx = self.createIndex(row, 0)
        self.dataChanged.emit(idx, idx, [ManagerTaskRole.StatusRole])
    
    def removeItem(self, index: QModelIndex):
        if 0 <= index.row() < len(self._actions):
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            del self._actions[index.row()]
            self.endRemoveRows()
            return True
        return False
    
    def findIndexItem(self, item):
        idx = self._actions.index(item)
        return self.createIndex(idx, 0)
    
    def getAction(self, idx):
        return self._actions[idx]
    
    def actions(self):
        return self._actions[:]
    
    def clear(self):
        self.beginResetModel()
        self._actions.clear()
        self.endResetModel()
    
    def rowCount(self, parent=None):
        return len(self._actions)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not (0 <= index.row() < len(self._actions)):
            return
        match role:
            case Qt.ItemDataRole.SizeHintRole:
                return QSize(-1, 50)
            case Qt.ItemDataRole.DisplayRole:
                return self._actions[index.row()].executor.description
            case ManagerTaskRole.StatusRole:
                return self._actions[index.row()].status.name
            case ManagerTaskRole.ExtraRole:
                return f"trig: {self._actions[index.row()].trigger.description}"
    
    def setData(self, index, value, role=Qt.ItemDataRole.DisplayRole):
        if not (0 <= index.row() < len(self._actions)):
            return
        match role:
            case ManagerTaskRole.StatusRole:
                self._actions[index.row()].status = value
    
    def setStatus(self, row, status: ActionStatus):
        idx = self.createIndex(row, 0)
        self.setData(idx, status, ManagerTaskRole.StatusRole)
        self.dataChanged.emit(idx, idx, [ManagerTaskRole.StatusRole])
    
    def __bool__(self):
        return bool(self._actions)
