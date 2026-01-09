from .volumeControl import VolumeControl

__version__ = (1, 0, 0)


def createWindow(parent):
    return VolumeControl(parent)
