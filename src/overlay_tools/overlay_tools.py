import subprocess
import sys
from pathlib import Path

import typer
from overlay_sdk import BaseProject

from unpacked import unpacked

app = typer.Typer()

creator = typer.Typer()
app.add_typer(creator, name="create", help="Создание определенного формата файлов")


@creator.command(name="setup", help="Создать setup.py")
def createSetup(
        kind: str = typer.Argument(..., help="Тип setup.py"),
        name: str = typer.Argument(..., help="Имя структуры"),
        dist: Path = typer.Argument(..., help="Куда сохранить")
):
    BaseProject.create_setup_file(kind, dist, {"name": name})


@creator.command(name="project", help="Создать проект")
def createProject(
        kind: str = typer.Argument(..., help="Тип проекта"),
        name: str = typer.Argument(..., help="Имя структуры"),
        dist: Path = typer.Argument(..., help="Куда сохранить")
):
    BaseProject.create_layout(kind, dist, {"name": name})


builder = typer.Typer()
app.add_typer(builder, name="build", help="Сборка файлов")


@builder.command(name="auto", help="Автоматическая сборка через setup.py")
def buildAuto():
    setup_file = Path.cwd() / "setup.py"
    if not setup_file.exists():
        typer.secho("Файл setup.py не найден. Используйте обычные команды.", fg="yellow")
        return
    
    try:
        subprocess.run([sys.executable, "setup.py"], check=True)
        typer.secho("Билд завершен успешно", fg="green")
    except Exception as e:
        typer.secho(f"Ошибка: {e}", fg="red")
        
        
@app.command(name="unpacked", help="Распаковка пакета")
def appUnpacked(
        path_output: Path = typer.Argument(..., help="Путь домашней паки Overlay"),
        *plugin_packs: Path
):
    try:
        for pack in plugin_packs:
            unpacked(pack, path_output)
            typer.secho(f"Пакет успешно распакован {pack.stem}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app(help_option_names=["--help", "-h"])
