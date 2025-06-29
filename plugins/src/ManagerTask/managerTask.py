from PySide6.QtWidgets import QTableWidgetItem, QMenu
from PySide6.QtCore import Qt, Signal, Slot, QThreadPool, QTimer, QDeadlineTimer

from API import Config, OverlayWidget, saveResource, loadResource

from .uis.main_ui import Ui_ManagerTask
from .dialogCreateTask import CreateDialogTask
from .tasks import Task, TaskStatus


class ManagerTask(OverlayWidget, Ui_ManagerTask):
    """Главный менеджер задач с Qt-интеграцией"""
    
    task_status_changed = Signal(int, TaskStatus)  # Сигнал изменения статуса задачи
    
    def __init__(self, parent):
        super().__init__(Config(__file__, "overlay_widget"), parent)
        self.setupUi(self)
        parent.addWidget(
            self,
            [Qt.AnchorPoint.AnchorHorizontalCenter, Qt.AnchorPoint.AnchorBottom]
        )
        
        QThreadPool.globalInstance().setMaxThreadCount(4)
        
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        
        self._tasks: list[Task] = []
        
        # Настройка таблицы
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self._show_context_menu)
        
        # Сигналы
        self.btnCreateTask.pressed.connect(self._create_task)
        self.task_status_changed.connect(self._update_task_status)
        
        # Таймер обновления задач
        self._setup_task_timer()
    
    @Slot(int, TaskStatus)
    def _update_task_status(self, row: int, status: TaskStatus):
        """Обновление UI должно происходить только в главном потоке"""
        if 0 <= row < self.tableWidget.rowCount():
            item = QTableWidgetItem(status.name)
            self.tableWidget.setItem(row, 2, item)
    
    def handler_tasks(self):
        if not self._tasks: return
        sorted_tasks = sorted(self._tasks, key=lambda t: t.priority, reverse=True)
        
        deadline = QDeadlineTimer(50)
        
        for task in sorted_tasks:
            if deadline.hasExpired():
                break
            
            task.update()
    
    def _setup_task_timer(self):
        """Настройка таймера для обработки задач"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.handler_tasks)
        self.timer.start(1000)  # Обновление каждую секунду
    
    def get_task(self, row: int) -> Task:
        """Получение задачи по строке таблицы"""
        item = self.tableWidget.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole)
    
    @Slot(int, TaskStatus)
    def _update_task_status(self, row: int, status: TaskStatus):
        """Обновление статуса задачи в таблице"""
        item = QTableWidgetItem(status.name)
        self.tableWidget.setItem(row, 2, item)
    
    def _create_task(self):
        """Создание новой задачи через диалог"""
        dialog = CreateDialogTask(self)
        if dialog.exec():
            task = dialog.getItem()
            self.add_task(task)
    
    def add_task(self, task: Task):
        """Добавление задачи в таблицу"""
        self._tasks.append(task)
        row = self.tableWidget.rowCount()
        task.status_changed.connect(lambda status: self._update_task_status(row, status))
        self.tableWidget.insertRow(row)
        
        # Создание элементов таблицы
        uid_item = QTableWidgetItem(task.uid)
        uid_item.setData(Qt.ItemDataRole.UserRole, task)
        
        name_item = QTableWidgetItem(task.name if len(task.name) >= 4 else "<unknown>")
        status_item = QTableWidgetItem(task.status.name)
        
        # Установка элементов в таблицу
        self.tableWidget.setItem(row, 0, uid_item)
        self.tableWidget.setItem(row, 1, name_item)
        self.tableWidget.setItem(row, 2, status_item)
    
    @Slot()
    def _show_context_menu(self, pos):
        """Показ контекстного меню для задачи"""
        item = self.tableWidget.itemAt(pos)
        if not item:
            return
        
        row = item.row()
        task = self.get_task(row)
        
        menu = QMenu(self)
        actions = {
            "delete": menu.addAction("Delete Task"),
            "cancel": menu.addAction("Cancel Task"),
            "restart": menu.addAction("Restart Task")
        }
        
        action = menu.exec(self.tableWidget.mapToGlobal(pos))
        
        if action == actions["delete"]:
            self.tableWidget.removeRow(row)
            self._tasks.remove(task)
        elif action == actions["cancel"]:
            task.cancel()
            self._update_task_status(row, task.status)
        elif action == actions["restart"]:
            task.restart()
            self._update_task_status(row, task.status)
    
    def loader(self):
        """Загрузка сохраненных задач"""
        try:
            tasks = loadResource(
                self.config.tasks.path,
                self.config
            )
            for task in tasks:
                self.add_task(task)
        except FileNotFoundError:
            pass
        super().loader()
    
    def savesConfig(self):
        """Сохранение текущих задач"""
        try:
            saveResource(
                self.config.tasks.path,
                self.config,
                self._tasks
            )
        except Exception as e:
            import traceback
            print(*traceback.format_exception(e))
        return super().savesConfig()
    
    def reloadConfig(self):
        """Перезагрузка конфигурации"""
        super().reloadConfig()
    
    def restoreConfig(self, config):
        """Восстановление конфигурации"""
        super().restoreConfig(config)
