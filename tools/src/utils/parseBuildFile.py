from pathlib import Path
from toml import load


def parseBuildFile(path: Path) -> dict:
    result = {}
    
    data = load(path)
    
    result["plugin.path"] = Path(data["plugin"]["path"])
    result["exclude.file"] = [exc_file for exc_file in data["build"]["exclude"] if not exc_file.startswith("/")]
    result["exclude.folder"] = [exc_folder.strip("/") for exc_folder in data["build"]["exclude"] if exc_folder.startswith("/")]
    result["platforms"] = data["platform"].get("available", ["all"])
    
    return result.copy()
