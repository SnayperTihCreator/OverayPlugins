import sys
import zipfile
from pathlib import Path
from zipfile import ZipFile

import toml
import typer


def smart_unpacked(plugin_path: Path, path_output: Path):
    current_platform = sys.platform  # 'win32' или 'linux'
    
    with zipfile.ZipFile(plugin_path) as zfile:
        # Читаем манифест прямо из архива
        if "plugin.toml" in zfile.namelist():
            with zfile.open("plugin.toml") as f:
                config = toml.load(f)
                supported = config.get("plugin", {}).get("platforms", [])
                
                if current_platform not in supported and "all" not in supported:
                    typer.secho(f" ПРЕДУПРЕЖДЕНИЕ: Плагин не поддерживает {current_platform}!", fg="yellow")
                    if not typer.confirm("Продолжить установку?"):
                        return
        
        # Вызов старой логики распаковки
        unpacked(plugin_path, path_output)
        typer.secho(f"Успешно распаковано: {plugin_path.name}", fg="green")


def unpacked(plugin_path: Path, path_output: Path):
    pluginFolder = path_output / "plugins"
    pluginFolder.mkdir(exist_ok=True)
    
    with ZipFile(plugin_path) as zfile:
        for entry in zfile.namelist():
            if entry.startswith("tools"):
                
                zfile.extract(entry, path_output)
            elif entry == "plugin.toml":
                continue
            else:
                zfile.extract(entry, pluginFolder)
