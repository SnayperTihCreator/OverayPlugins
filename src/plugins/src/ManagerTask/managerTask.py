from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt, Slot, QThreadPool, QDeadlineTimer

from oapi import Config, OWidget

from OExtension.yaml_storage import Storage

from .uis.main_ui import Ui_ManagerTask
from .dialogCreateTask import CreateDialogTask
from .tasks import TaskStatus
from .dialogAction import DialogAction
from .config import ManagerTaskConfig
from .modelData import ModelTask, ManagerTaskDelegate, ManagerTaskRole


class ManagerTask(OWidget, Ui_ManagerTask):
    """Главный менеджер задач с Qt-интеграцией"""
    
    def __init__(self, parent):
        super().__init__(Config("ManagerTask", "widget", scheme=ManagerTaskConfig), parent)
        self.setupUi(self)
        self.gridOverlay(
            Qt.AnchorPoint.AnchorHorizontalCenter,
            Qt.AnchorPoint.AnchorBottom
        )
        self._storage = Storage()
        QThreadPool.globalInstance().setMaxThreadCount(4)
        
        self._tasksModel = ModelTask()
        self._tasksModel.dataChanged.connect(self._on_data_change)
        self._delegate = ManagerTaskDelegate(self.listView)
        self.listView.setItemDelegate(self._delegate)
        self.listView.setModel(self._tasksModel)
        
        self.listView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self._show_context_menu)
        
        # Сигналы
        self.btnCreateTask.pressed.connect(self._create_task)
        
    def _on_data_change(self, idx1, idx2, roles):
        if ManagerTaskRole.StatusRole in roles:
            self.saveTasks()
        
    def saveTasks(self):
        try:
            with open(f"pldata://{self.config.name}/{self.config.data.tasks.path}", "w", encoding="utf-8") as file:
                self._storage.dump(self._tasksModel.tasks(), file)
        except Exception as e:
            import traceback
            print(*traceback.format_exception(e))
    
    def __process__(self):
        if not self._tasksModel:
            return
        sorted_tasks = self._tasksModel.s_tasks()

        deadline = QDeadlineTimer(50)

        for task in sorted_tasks:
            if deadline.hasExpired():
                break

            task.update()
    
    def _create_task(self):
        """Создание новой задачи через диалог"""
        dialog = CreateDialogTask(self)
        if dialog.exec():
            self._tasksModel.addTask(dialog.getItem())
    
    @Slot()
    def _show_context_menu(self, pos):
        """Показ контекстного меню для задачи"""
        idx = self.listView.indexAt(pos)
        if not idx:
            return
        task = self._tasksModel.getTask(idx.row())

        menu = QMenu(self)
        actions = {
            "delete": menu.addAction("Delete Task"),
            "cancel": menu.addAction("Cancel Task") if not task.is_finish() else None,
            "restart": menu.addAction("Restart Task") if task.status != TaskStatus.IDLE else None,
            "show_action": menu.addAction("Show actions")
        }

        action = menu.exec(self.listView.mapToGlobal(pos))

        if action == actions["delete"]:
            self._tasksModel.removeItem(idx)
        elif action == actions["cancel"]:
            task.cancel()
        elif action == actions["restart"]:
            task.restart()
        elif action == actions["show_action"]:
            dialog = DialogAction(task.actions, self)
            dialog.show()
    
    def __ready__(self):
        """Загрузка сохраненных задач"""
        try:
            with open(f"pldata://{self.config.name}/{self.config.data.tasks.path}", encoding="utf-8") as file:
                tasks = self._storage.load(file)
            for task in tasks:
                self._tasksModel.addTask(task)
        except FileNotFoundError as e:
            print(type(e), e)
        super().__ready__()
        
    def save_status(self):
        self.saveTasks()
        return super().save_status()
