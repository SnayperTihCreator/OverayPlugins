from .virtualizationWidget import Virtualization

__version__ = (1, 1, 0)

def createWindow(parent):
    return Virtualization(parent)
