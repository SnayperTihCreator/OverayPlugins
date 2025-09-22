from pathlib import Path

from .util import buildEnv, buildFileContent, getAppPath

env = buildEnv(getAppPath() / "datas/ThemeFolder.xml")


def createFolderTheme(name: str, root: Path):
    folder = root / name
    folder.mkdir(exist_ok=True, parents=True)
    
    configFile = folder / "theme.toml"
    themeFile = folder / "theme.py"
    
    contentConfigFile = env.get_template("theme.toml").render(themeName=name)
    contentThemeFile = env.get_template("theme.py").render(themeName=name)
    
    buildFileContent(configFile, contentConfigFile)
    buildFileContent(themeFile, contentThemeFile)
