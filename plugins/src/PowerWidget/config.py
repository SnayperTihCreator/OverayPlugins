from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from API.defaultConfigs import ConfigWindow


@dataclass(frozen=True)
class ChapterPowerFormat:
    unitFormat: str = Field("%u%")


class PowerWidgetConfig(ConfigWindow):
    powerFormat: ChapterPowerFormat = field(default_factory=ChapterPowerFormat)
