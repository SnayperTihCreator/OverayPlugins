from fnmatch import fnmatch
from pathlib import Path


def excludeFolder(path: Path, exc_folders: list[Path]):
    for exc_folder in exc_folders:
        if exc_folder in path.parts: return True
    return False


def excludeFile(path: Path, exc_files: list[Path], exc_folders: list[Path]):
    if excludeFolder(path, exc_folders):
        return True
    for exc_file in exc_files:
        if fnmatch(str(path), str(exc_file)): return True
    return False
