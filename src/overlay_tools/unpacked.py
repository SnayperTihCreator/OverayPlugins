from pathlib import Path
from zipfile import ZipFile


def unpacked(plugin_path: Path, path_output: Path):
    pluginFolder = path_output/"plugins"
    pluginFolder.mkdir(exist_ok=True)
    
    with ZipFile(plugin_path) as zfile:
        for entry in zfile.namelist():
            if entry.startswith("tools"):
                
                zfile.extract(entry, path_output)
            elif entry == "plugin.toml":
                continue
            else:
                zfile.extract(entry, pluginFolder)
            
