from pathlib import Path
from zipfile import ZipFile


def buildTheme(pathInput: Path, pathOutput: Path):
    themeName = pathInput.name
    
    resultFile = pathOutput / "compress" / f"{themeName}.overtheme"
    resultFile.parent.mkdir(parents=True, exist_ok=True)
    
    with ZipFile(resultFile, "w") as zfile:
        for entry in pathInput.rglob("*"):
            arcname = str(entry.relative_to(pathInput))
            if entry.is_file():
                zfile.write(entry, arcname)
            elif entry.is_dir():
                zfile.mkdir(arcname)
                
    return resultFile
    