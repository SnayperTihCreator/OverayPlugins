from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from oapi import default_configs


@dataclass
class ChapterClockFormat:
    date_format: str = field(default="dd/MM/yyyy")
    time_format: str = field(default="hh:mm:ss")


class ClockDateConfig(default_configs.PluginConfig):
    clock_format: ChapterClockFormat = Field(default_factory=ChapterClockFormat)
