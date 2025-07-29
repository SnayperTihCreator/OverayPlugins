from pathlib import Path

from .util import toCamelCase

dataConfigWindow = """
[window]
width = 220
height = 75
styleFile = "style.css"
opacity = 1
"""

dataConfigWidget = """
[widget]
styleFile = "style.css"
"""

dataHeader = """
from .{pluginNameCamel} import {pluginName}

"""

dataInitWindow = """
def createWindow(parent):
    return {pluginName}(parent)
"""

dataInitWidget = """
def createWidget(parent):
    return {pluginName}(parent)
"""


def createFolderPlugin(name: str, root: Path, types: list):
    nameCamel = toCamelCase(name)
    
    folder = root / name
    initFile = folder / "__init__.py"
    mainFile = folder / f"{nameCamel}.py"
    configFile = folder / "config.toml"
    styleFile = folder / "style.css"
    
    folder.mkdir(exist_ok=True)
    initFile.touch(exist_ok=True)
    mainFile.touch(exist_ok=True)
    configFile.touch(exist_ok=True)
    styleFile.touch(exist_ok=True)
    
    dataInit = dataHeader.format(pluginNameCamel=nameCamel, pluginName=name)
    dataConfig = ""
    if "window" in types:
        dataInit += dataInitWindow.format(pluginNameCamel=nameCamel, pluginName=name)
        dataConfig += dataConfigWindow
    if "widget" in types:
        dataInit += dataInitWidget.format(pluginNameCamel=nameCamel, pluginName=name)
        dataConfig += dataConfigWidget
    
    initFile.write_text(dataInit, "UTF-8")
    configFile.write_text(dataConfig)
