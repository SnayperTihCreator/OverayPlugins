from pathlib import Path
from zipfile import ZipFile

from toml import dumps

from .util import excludeFile, excludeFolder


def buildPack(data: dict, plugin: Path, pathOutput: Path):
    pluginName = data["plugin.path"].name
    
    resultFile = pathOutput / "pack" / f"{pluginName}.pack"
    resultFile.parent.mkdir(parents=True, exist_ok=True)
    
    toolsFolder = pathOutput / "tools"
    tWinFolder = toolsFolder / f"windows-{pluginName}"
    tLinuxFolder = toolsFolder / f"linux-{pluginName}"
    
    with ZipFile(resultFile, "w") as zfile:
        zfile.write(plugin, plugin.name)
        zfile.mkdir("tools")
        zfile.mkdir("tools/windows")
        zfile.mkdir("tools/linux")
        
        module_win = []
        module_linux = []
        
        if tWinFolder.exists():
            for entry in tWinFolder.rglob("*"):
                arcname = f"tools/windows/{entry.relative_to(tWinFolder)}"
                if entry.is_file():
                    zfile.write(entry, arcname)
                elif entry.is_dir():
                    zfile.mkdir(arcname)
            for file in tWinFolder.iterdir():
                if file.is_dir() and (file / "__init__.py").exists():
                    module_win.append(file.name)
        
        if tLinuxFolder.exists():
            for entry in tLinuxFolder.rglob("*"):
                arcname = f"tools/linux/{entry.relative_to(tLinuxFolder)}"
                if entry.is_file():
                    zfile.write(entry, arcname)
                elif entry.is_dir():
                    zfile.mkdir(arcname)
            
            for file in tLinuxFolder.iterdir():
                if file.is_dir() and (file / "__init__.py").exists():
                    module_linux.append(file.name)
        
        metadata = {
            "plugin": {
                "name": pluginName,
                "version": data.get("plugin.version", "1.0.0"),
                "author": data.get("plugin.author", "Unknown"),
                "description": data.get("plugin.description", ""),
                "platforms": data["platforms"]
            },
            "tools": {
                "win32": module_win,
                "linux": module_linux
            }
        }
        
        zfile.writestr("plugin.toml", dumps(metadata))
    return resultFile
