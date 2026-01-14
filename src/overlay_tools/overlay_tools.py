import subprocess
import sys
from pathlib import Path

import typer
from overlay_sdk import BaseProject

from unpacked import smart_unpacked

app = typer.Typer()


@app.command(name="create-setup", help="Создать setup.py")
def createSetup(
        kind: str = typer.Argument(..., help="Тип setup.py"),
        name: str = typer.Argument(..., help="Имя структуры"),
        dist: Path = typer.Argument(..., help="Куда сохранить")
):
    BaseProject.create_setup_file(kind, dist, {"name": name})


@app.command(name="unpacked", help="Распаковка пакета")
def appUnpacked(
        path_output: Path = typer.Argument(..., help="Путь домашней паки Overlay"),
        *plugin_packs: Path
):
    try:
        for pack in plugin_packs:
            smart_unpacked(pack, path_output)
            typer.secho(f"Пакет успешно распакован {pack.stem}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@app.command(name="build")
def appBuild():
    """Запускает сборку текущего проекта через setup.py"""
    import subprocess
    import sys
    if Path("setup.py").exists():
        subprocess.run([sys.executable, "setup.py", "build"])
    else:
        typer.secho("setup.py не найден!", fg="red")


@app.command(name="new")
def appNew(kind: str, name: str, path: Path = Path(".")):
    """Создает новый проект с setup.py и шаблонами"""
    BaseProject.create_layout(kind, path / name, {"name": name})
    BaseProject.create_setup_file(kind, path / name, {"name": name})
    typer.secho(f"Проект {name} ({kind}) готов!", fg="green")


if __name__ == "__main__":
    app(help_option_names=["--help", "-h"])
