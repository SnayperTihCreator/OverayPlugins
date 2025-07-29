from pathlib import Path


def createToolsFolder(name: str, platform: str, path: Path):
    folder = path / "tools"
    folder.mkdir(exist_ok=True)
    
    if platform == "win32":
        toolsWin = folder / f"windows-{name}"
        toolsWin.mkdir(exist_ok=True)
    if platform == "linux":
        toolsLinux = folder / f"linux-{name}"
        toolsLinux.mkdir(exist_ok=True)
