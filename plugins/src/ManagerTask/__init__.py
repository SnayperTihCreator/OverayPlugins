from .managerTask import ManagerTask

__version__ = [1, 0, 0]


def createWidget(parent):
    return ManagerTask(parent)
