from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from API.defaultConfigs import ConfigWidget


@dataclass(frozen=True)
class ChapterTasks:
    path: str = Field("tasks.yml")


class ManagerTaskConfig(ConfigWidget):
    tasks: ChapterTasks = field(default_factory=ChapterTasks)
