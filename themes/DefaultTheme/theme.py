from PySide6.QtGui import QColor, QFont

from ColorControl.theme import Theme
from API.config import Config

from attrs import define, field

ThemeConfig = Config("DefaultTheme", "theme", "theme")
@define
class DefaultTheme(Theme):
    baseColor: QColor = field(default=QColor(ThemeConfig.data.colors.base))
    mainTextColor: QColor = field(default=QColor(ThemeConfig.data.colors.main_text))
    altTextColor: QColor = field(default=QColor(ThemeConfig.data.colors.alt_text))
    font: QFont = field(default=QFont("Montserrat", 12, 700))
    
    def preInitTheme(self, *args): ...
    
    def postInitTheme(self, *args): ...