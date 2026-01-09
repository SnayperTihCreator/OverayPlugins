from pydantic.dataclasses import dataclass
from dataclasses import field
from pydantic import Field

from oapi import default_configs


@dataclass(frozen=True)
class ChapterIcons:
    size: int = Field(30, gt=0, lt=128)
    modulate: str = Field("#fff", pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8})$')


class PlayerControlConfig(default_configs.PluginConfig):
    icons: ChapterIcons = field(default_factory=ChapterIcons)
