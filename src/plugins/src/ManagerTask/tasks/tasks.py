from enum import Enum, auto
from typing import Any

from attrs import define, field

from OExtension.yaml_storage import yaml_enum_serialized, YamlSerialized
from .signals import Signal
from .actions import Action, ActionStatus


@yaml_enum_serialized
class TaskStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    PARTIAL = auto()
    ABORTED = auto()
    
    @classmethod
    def restore(cls, data):
        return cls(int(data))
    
    def save(self):
        return str(self.value)


@define(slots=False)
class Task(YamlSerialized):
    """Реализация Task с сохранением оригинальной логики и Qt-интеграцией"""
    
    # Сигналы состояния
    status_changed = Signal(TaskStatus)  # TaskStatus
    
    name: str = field()
    uid: str = field()
    actions: list[Action] = field(factory=list)
    priority: int = field(default=0)
    
    status: TaskStatus = field(default=TaskStatus.IDLE, init=False)
    
    def __attrs_post_init__(self):
        super().__init__()
    
    def _update_status(self, new_status):
        """Обновление статуса с уведомлением"""
        if self.status != new_status:
            self.status = new_status
            self.status_changed.emit(new_status)
    
    def update(self):
        if self.is_finish():
            return
        
        if self.status == TaskStatus.IDLE:
            self._update_status(TaskStatus.ACTIVE)
        
        # Обновляем все действия
        for action in self.actions:
            action.update()
        
        # Анализ результатов
        compiled = skipped = failed = 0
        for action in self.actions:
            if action.status == ActionStatus.SUCCESS:
                compiled += 1
            elif action.status == ActionStatus.CANCELLED:
                skipped += 1
            elif action.status == ActionStatus.FAILED:
                failed += 1
        
        # Определение общего статуса
        if compiled == len(self.actions):
            self._update_status(TaskStatus.COMPLETED)
        elif compiled + skipped + failed == len(self.actions):
            self._update_status(TaskStatus.PARTIAL)
    
    def cancel(self):
        """Отмена задачи"""
        self._update_status(TaskStatus.ABORTED)
        for action in self.actions:
            action.cancel()
    
    def restart(self):
        """Перезапуск задачи"""
        for action in self.actions:
            action.restart()
        self._update_status(TaskStatus.IDLE)
    
    def is_finish(self):
        """Проверка завершенности задачи"""
        return self.status in {TaskStatus.PARTIAL,
                               TaskStatus.COMPLETED,
                               TaskStatus.ABORTED}
    
    @classmethod
    def restore(cls, data):
        """Восстановление из сохраненных данных"""
        obj = cls(data["name"], data["uid"], data["actions"].copy())
        obj.status = TaskStatus(data["status"])
        return obj
    
    def save(self):
        """Сохранение состояния задачи"""
        return {
            "name": self.name,
            "uid": self.uid,
            "actions": self.actions.copy(),
            "status": self.status,
        }
