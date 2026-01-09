from pathlib import Path
from zipfile import ZipFile

from .util import excludeFile, excludeFolder


def buildPlugin(data: dict, pathOutput: Path):
    pluginName = data["plugin.path"].name
    
    pluginFolder: Path = data["plugin.path"]
    
    resultFile = pathOutput/"compress"/f"{pluginName}.plugin"
    resultFile.parent.mkdir(parents=True, exist_ok=True)
    
    exc_file = data["exclude.file"]+["*.tmp"]
    exc_folder = data["exclude.folder"]+["__pycache__"]
    
    with ZipFile(resultFile, "w") as zfile:
        zfile.mkdir(pluginName)
        for file in pluginFolder.rglob("*"):
            rfile = file.relative_to(pluginFolder)
            if file.is_dir() and excludeFolder(rfile, exc_folder):
                continue
            elif file.is_file() and excludeFile(rfile, exc_file, exc_folder):
                continue
            
            if file.suffix == ".py":
                zfile.write(file, pluginName/rfile)
            else:
                zfile.write(file, rfile)
    
    return resultFile
