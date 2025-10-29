from collections import namedtuple
from pathlib import Path

from .util import buildEnv, buildFileContent, getAppPath

env = buildEnv(getAppPath() / "datas/OAddonsFolder.xml")
DataRender = namedtuple("DataRender", ["platform", "window"])


def createFolderOAddons(name: str, root: Path, platform: str, window: str):
    dr = DataRender(platform, window)
    
    folder = root / f"{name}_{platform}_{window}"
    initFile = folder / "__init__.py"
    metadataFile = folder / "metadata.toml"
    
    folder.mkdir(exist_ok=True)
    
    contentInitFile = env.get_template("__init__.py").render(data=dr, pluginName=name)
    contentMetadataFile = env.get_template("metadata.toml").render(data=dr, name=name)
    
    buildFileContent(initFile, contentInitFile)
    buildFileContent(metadataFile, contentMetadataFile)
