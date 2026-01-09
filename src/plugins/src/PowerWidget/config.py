from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from oapi import default_configs


@dataclass(frozen=True)
class ChapterPowerFormat:
    unitFormat: str = Field("%u%")


class PowerWidgetConfig(default_configs.PluginConfig):
    powerFormat: ChapterPowerFormat = field(default_factory=ChapterPowerFormat)
