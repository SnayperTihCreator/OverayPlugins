from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from API.defaultConfigs import ConfigWindow


@dataclass
class ChapterClockFormat:
    dateFormat: str = field(default="dd/MM/yyyy")
    timeFormat: str = field(default="hh:mm:ss")


class ClockDateConfig(ConfigWindow):
    clockFormat: ChapterClockFormat = Field(default_factory=ChapterClockFormat)
