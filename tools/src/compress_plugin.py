from zipfile import ZipFile
from pathlib import Path
import toml


def compress_plugin(plugin_path, build_dir, out_dir, toml_data):
    plugin_path = Path(plugin_path)
    plugin_name = plugin_path.name
    with ZipFile(f"{out_dir}/{plugin_name}.plugin", "w") as zfile:
        data = {
            "plugin": {
                "name": plugin_name,
                "version": toml_data["plugin"].get("version", "1.0.0"),
                "author": toml_data["plugin"].get("author", "Unknown"),
                "description": toml_data["plugin"].get("description", ""),
                "platforms": toml_data["platform"].get("available", ["all"])
            },
            "tools": {
                "win32": [],
                "linux": []
            }
        }
        with zfile.open("plugin.toml", "w") as pluginFile:
            pluginFile.write(toml.dumps(data).encode("utf-8"))
        zfile.write(Path(build_dir)/(plugin_name+".zip"), plugin_name+".zip")
        tools_folder = plugin_path.parent/"tools"
        tWin32Folder = tools_folder/f"windows-{plugin_name}"
        zfile.mkdir("tools/windows")
        tLinuxFolder = tools_folder/f"linux-{plugin_name}"
        zfile.mkdir("tools/linux")
        if tWin32Folder.exists():
            for entry in tWin32Folder.rglob("*"):
                arcname = f"tools/windows/{entry.relative_to(tWin32Folder)}"
                if entry.is_file():
                    zfile.write(entry, arcname)
                elif entry.is_dir():
                    zfile.mkdir(arcname)
        if tLinuxFolder.exists():
            for entry in tLinuxFolder.rglob("*"):
                arcname = f"tools/linux/{entry.relative_to(tLinuxFolder)}"
                if entry.is_file():
                    zfile.write(entry, arcname)
                elif entry.is_dir():
                    zfile.mkdir(arcname)
        return zfile.filename