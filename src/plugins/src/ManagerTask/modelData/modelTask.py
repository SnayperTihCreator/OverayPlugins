from functools import partial

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QSize

from ..tasks import Task, TaskStatus
from .core import ManagerTaskRole


class ModelTask(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._tasks: list[Task] = []
        self._tasks_uid: list[str] = []
    
    def addTask(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError
        self.beginInsertRows(QModelIndex(), len(self._tasks), len(self._tasks))
        if task.uid in self._tasks_uid:
            self.endInsertRows()
            return
        self._tasks.append(task)
        self._tasks_uid.append(task.uid)
        task.status_changed.connect(partial(self._on_handled_update_status, task))
        self.endInsertRows()
        
    def _on_handled_update_status(self, task, _status):
        row = self._tasks.index(task)
        idx = self.createIndex(row, 0)
        self.dataChanged.emit(idx, idx, [ManagerTaskRole.StatusRole])
    
    def removeItem(self, index: QModelIndex):
        if 0 <= index.row() < len(self._tasks):
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            del self._tasks[index.row()]
            del self._tasks_uid[index.row()]
            self.endRemoveRows()
            return True
        return False
    
    def findIndexItem(self, item):
        idx = self._tasks.index(item)
        return self.createIndex(idx, 0)
    
    def getTask(self, idx):
        return self._tasks[idx]
    
    def tasks(self):
        return self._tasks[:]
    
    def s_tasks(self):
        return sorted(self._tasks, key=lambda t: t.priority, reverse=True)
    
    def clear(self):
        self.beginResetModel()
        self._tasks.clear()
        self.endResetModel()
    
    def rowCount(self, parent=None):
        return len(self._tasks)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not (0 <= index.row() < len(self._tasks)):
            return
        match role:
            case Qt.ItemDataRole.SizeHintRole:
                return QSize(-1, 50)
            case Qt.ItemDataRole.DisplayRole:
                return self._tasks[index.row()].name
            case ManagerTaskRole.StatusRole:
                return self._tasks[index.row()].status.name
            case ManagerTaskRole.ExtraRole:
                return f"id: {self._tasks[index.row()].uid}"
    
    def setData(self, index, value, role=Qt.ItemDataRole.DisplayRole):
        if not (0 <= index.row() < len(self._tasks)):
            return
        match role:
            case ManagerTaskRole.StatusRole:
                self._tasks[index.row()].status = value
    
    def setStatus(self, row, status: TaskStatus):
        idx = self.createIndex(row, 0)
        self.setData(idx, status, ManagerTaskRole.StatusRole)
        self.dataChanged.emit(idx, idx, [ManagerTaskRole.StatusRole])
    
    def __bool__(self):
        return bool(self._tasks)
