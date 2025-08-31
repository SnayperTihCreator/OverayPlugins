from .visualisationWidget import Visualisation


__version__ = (1, 1, 0)


def createWindow(parent):
    return Visualisation(parent)
