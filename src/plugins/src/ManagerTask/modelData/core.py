from enum import IntEnum, auto
from PySide6.QtCore import Qt


class ManagerTaskRole(IntEnum):
    StatusRole = Qt.ItemDataRole.UserRole
    ExtraRole = auto()
