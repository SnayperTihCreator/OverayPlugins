from pathlib import Path

configTheme = """
[theme]
name = "{themeName}"
[colors]
base = "#6e738d" # Базовый фон
main_text = "#cad3f5" # Основной текст
alt_text = "#8aadf4" # Второй текст
"""

themeData = """
from PySide6.QtGui import QColor, QFont

from ColorControl.theme import Theme
from API.config import Config

from attrs import define, field

ThemeConfig = Config("{themeName}", "theme", "theme")
@define
class {themeName}(Theme):
    baseColor: QColor = field(default=QColor(ThemeConfig.data.colors.base))
    mainTextColor: QColor = field(default=QColor(ThemeConfig.data.colors.main_text))
    altTextColor: QColor = field(default=QColor(ThemeConfig.data.colors.alt_text))
    font: QFont = field(default=QFont("Montserrat", 12, 700))
    
    def preInitTheme(self, *args): ...
    
    def postInitTheme(self, *args): ...
"""


def createFolderTheme(name: str, root: Path):
    folder = root / name
    folder.mkdir(exist_ok=True, parents=True)
    
    configFile = folder / "theme.toml"
    configFile.touch(exist_ok=True)
    configFile.write_text(configTheme.format(themeName=name), encoding="utf-8")
    
    themeFile = folder / "theme.py"
    themeFile.touch(exist_ok=True)
    themeFile.write_text(themeData.format(themeName=name), encoding="utf-8")
