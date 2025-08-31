import re

from pydantic.dataclasses import dataclass
from pydantic import Field

from .commonConfig import ChapterNameResource, BaseConfig

pattern_color = re.compile(r"#[0-9a-fA-f][0-9a-fA-f][0-9a-fA-f]"
                           r"[0-9a-fA-f][0-9a-fA-f][0-9a-fA-f]")


@dataclass(frozen=True)
class ChapterColors:
    base: str = Field("#6e738d", pattern=pattern_color)
    main_text: str = Field("#cad3f5", pattern=pattern_color)
    alt_text: str = Field("#8aadf4", pattern=pattern_color)


class ConfigTheme(BaseConfig):
    theme: ChapterNameResource = Field(default_factory=ChapterNameResource)
    colors: ChapterColors = Field(default_factory=ChapterColors)
