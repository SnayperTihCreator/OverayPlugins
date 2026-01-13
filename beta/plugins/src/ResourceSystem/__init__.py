from .resourceSystem import ResourceSystem

__version__ = (1, 0, 0)


def createWindow(parent):
    return ResourceSystem(parent)
