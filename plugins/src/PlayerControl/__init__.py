from .playerControl import PlayerControl

__version__ = (1, 3, 0)


def createWindow(parent):
    return PlayerControl(parent)

