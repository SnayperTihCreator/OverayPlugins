from .powerWidget import PowerWidget

__version__ = (1, 0, 3)


def createWindow(parent):
    return PowerWidget(parent)
