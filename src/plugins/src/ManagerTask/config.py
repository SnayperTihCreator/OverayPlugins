from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from oapi import default_configs


@dataclass(frozen=True)
class ChapterTasks:
    path: str = Field("tasks.yml")


class ManagerTaskConfig(default_configs.PluginConfig):
    tasks: ChapterTasks = field(default_factory=ChapterTasks)
