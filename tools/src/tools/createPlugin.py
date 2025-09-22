from collections import namedtuple
from pathlib import Path

from .util import toCamelCase, buildEnv, buildFileContent, getAppPath

env = buildEnv(getAppPath() / "datas/PluginFolder.xml")
DataRender = namedtuple("DataRender", ["isWidget", "isWindow"])


def createFolderPlugin(name: str, root: Path, types: list):
    nameCamel = toCamelCase(name)
    dr = DataRender("widget" in types, "window" in types)
    
    folder = root / name
    initFile = folder / "__init__.py"
    mainFile = folder / f"{nameCamel}.py"
    configFile = folder / "config.toml"
    styleFile = folder / "style.css"
    metadataFile = folder / "metadata.toml"
    
    folder.mkdir(exist_ok=True)
    
    contentInitFile = env.get_template("__init__.py").render(data=dr, pluginName=name)
    contentMainFile = ""
    contentConfigFile = env.get_template("config.toml").render(data=dr, pluginName=name)
    contentStyleFile = ""
    contentMetadataFile = env.get_template("metadata.toml").render(data=dr, pluginName=name)
    
    buildFileContent(initFile, contentInitFile)
    buildFileContent(mainFile, contentMainFile)
    buildFileContent(configFile, contentConfigFile)
    buildFileContent(styleFile, contentStyleFile)
    buildFileContent(metadataFile, contentMetadataFile)
