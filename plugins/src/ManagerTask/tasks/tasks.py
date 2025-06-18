from enum import Enum, auto

import yaml
from attrs import define, field

from .core import ABCObject, registry_from_yaml, registry_to_yaml
from .actions import Action, ActionStatus


class TaskStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    PARTIAL = auto()
    PARTIAL_WITH_ERROR = auto()
    ABORTED = auto()
    
    @classmethod
    def to_yaml(cls, dumper: yaml.Dumper, data):
        return dumper.represent_scalar("!TaskStatus", str(data.value))
    
    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node):
        data = loader.construct_scalar(node)
        return cls(int(data))


registry_to_yaml(yaml.SafeDumper, TaskStatus, TaskStatus.to_yaml)
registry_from_yaml(yaml.SafeLoader, "!TaskStatus", TaskStatus.from_yaml)


@define
class Task(ABCObject):
    name: str = field()
    uid: int = field()
    actions: list[Action] = field(factory=list)
    status: TaskStatus = field(default=TaskStatus.IDLE, init=False)
    
    def update(self, *args, **kwargs):
        if self.status in [TaskStatus.COMPLETED, TaskStatus.PARTIAL_WITH_ERROR, TaskStatus.PARTIAL]:
            return
        
        if self.status == TaskStatus.IDLE:
            self.status = TaskStatus.ACTIVE
            for action in self.actions:
                action.clear()
        
        for action in self.actions:
            action.update(*args, **kwargs)
            
        compiled = 0
        skipped = 0
        failed = 0
        for action in self.actions:
            if action.status == ActionStatus.SUCCESS:
                compiled += 1
            if action.status == ActionStatus.CANCELLED:
                skipped += 1
            if action.status == ActionStatus.FAILED:
                failed += 1
        if compiled == len(self.actions):
            self.status = TaskStatus.COMPLETED
        if compiled+skipped == len(self.actions):
            self.status = TaskStatus.PARTIAL
        if compiled+skipped+failed == len(self.actions):
            self.status = TaskStatus.PARTIAL_WITH_ERROR
    
    def cancel(self):
        for action in self.actions:
            action.cancel()
        self.status = TaskStatus.ABORTED
        
    def is_compiled(self):
        return self.status in [TaskStatus.PARTIAL_WITH_ERROR, TaskStatus.PARTIAL, TaskStatus.COMPLETED]
    
    @classmethod
    def restore(cls, data):
        obj = cls(data["name"], data["uid"])
        obj.actions = data["actions"].copy()
        obj.status = data["status"]
        return obj
    
    def save(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "actions": self.actions.copy(),
            "status": self.status
        }
