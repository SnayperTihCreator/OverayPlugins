from .clockDateWidget import ClockDateWidget

__version__ = (1, 0, 0)


def createWindow(parent):
    return ClockDateWidget(parent)
