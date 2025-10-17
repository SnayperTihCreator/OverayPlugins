from pathlib import Path
from toml import dumps

from .util import toCamelCase


def createBuildFile(name: str, pathPlugin: Path, root: Path, platforms: list = None, exclude: list = None):
    data = {
        "plugin": {
            "path": pathPlugin.as_posix()
        },
        "build": {
            "exclude": exclude or []
        },
        "platform": {}
    }
    if platforms is not None:
        data["platform"]["available"] = [platforms]
    
    buildFile = root / (toCamelCase(name) + ".toml")
    buildFile.touch(exist_ok=True)
    
    buildFile.write_text(dumps(data), "UTF-8")
