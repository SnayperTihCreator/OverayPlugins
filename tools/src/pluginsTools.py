from pathlib import Path
from enum import StrEnum, auto

import typer

import tools
import utils


class Platform(StrEnum):
    Win32 = auto()
    Linux = auto()


app = typer.Typer()

creator = typer.Typer()
app.add_typer(creator, name="create", help="Создание определенного формата файлов")


@creator.command(name="plugin", help="Создать папку плагина")
def createPlugin(
        name: str = typer.Argument(..., help="Имя плагина"),
        path: Path = typer.Argument(..., help="Путь корневой папки плагина"),
        isWindow: bool = typer.Option(False, "--window", "-wn", help="Плавающие окно"),
        isWidget: bool = typer.Option(False, "--widget", "-wg", help="Виджет в самом Overlay")
):
    types = []
    if isWindow:
        types.append("window")
    if isWidget:
        types.append("widget")
    try:
        tools.createFolderPlugin(name, path.absolute(), types)
        typer.secho("Репозиторий плагина создан", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@creator.command(name="tools", help="Создать папку зависимостей")
def createTools(
        name: str = typer.Argument(..., help="Имя плагина"),
        platform: Platform = typer.Argument(..., help="Платформа для зависимостей"),
        path: Path = typer.Argument(..., help="Путь к корневой папки плагина"),
):
    try:
        tools.createToolsFolder(name, platform, path.absolute())
        typer.secho(f"Папка для зависимостей:{name}\nСоздана", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@creator.command(name="build-file", help="Файл для сборки плагина в пакет")
def createBuildFile(
        name: str = typer.Argument(..., help="Имя плагина"),
        path: Path = typer.Argument(..., help="Путь куда сохранить"),
        path_plugin: Path = typer.Argument(..., help="Путь к плагину"),
        exclude: str = typer.Argument(None, help="Все что исключить(больше одного через ';')"),
        platforms: str = typer.Argument(None, help="Платформы(через ';')")
):
    try:
        exclude = exclude or ""
        exclude = exclude.split(";")
        
        platforms = platforms or ""
        platforms = platforms.split(";")
        
        tools.createBuildFile(name, path_plugin, path, platforms, exclude)
        typer.secho(f"Создан в {path}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@creator.command(name="theme", help="Создать папку темы")
def createThemeFolder(
        name: str = typer.Argument(..., help="Имя темы"),
        path: Path = typer.Argument(..., help="Путь куда сохранить")
):
    try:
        tools.createFolderTheme(name, path)
        typer.secho(f"Создан в {path}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


builder = typer.Typer()
app.add_typer(builder, name="build", help="Сборка файлов")


@builder.command(name="plugin", help="Собрать плагин")
def buildPlugin(
        build_file: Path = typer.Argument(..., help="Путь к файлу сборки"),
        path_output: Path = typer.Argument(..., help="Выходная папка"),

):
    dataToml = utils.parseBuildFile(build_file)
    try:
        result = utils.buildPlugin(dataToml, path_output)
        typer.secho(f"Плагин успешно собран {result}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)
        
        
@builder.command(name="oaddons", help="Собрать Overlay дополнение")
def buildOAddons(
        build_file: Path = typer.Argument(..., help="Путь к файлу сборки"),
        path_output: Path = typer.Argument(..., help="Выходная папка"),

):
    dataToml = utils.parseBuildFile(build_file)
    try:
        result = utils.buildOAddons(dataToml, path_output)
        typer.secho(f"Overlay дополнение успешно собран {result}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@builder.command(name="pack", help="Собрать пакет")
def buildPack(
        build_file: Path = typer.Argument(..., help="Путь к файлу сборки", ),
        path_output: Path = typer.Argument(..., help="Выходная папка"),
        path_plugin: Path = typer.Argument(Path("../../themes/compress"), help="Путь к собранному плагину"),
):
    dataToml = utils.parseBuildFile(build_file)
    try:
        plugin = utils.buildPlugin(dataToml, path_plugin)
        pack = utils.buildPack(dataToml, plugin, path_output)
        typer.secho(f"Пакет успешно собран {pack}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@builder.command(name="theme", help="Собрать тему")
def buildTheme(
        folder_input: Path = typer.Argument(..., help="Путь к папке темы"),
        path_output: Path = typer.Argument(..., help="Выходная папка")
):
    try:
        theme = utils.buildTheme(folder_input, path_output)
        typer.secho(f"Тема успешно собрана {theme}", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


@app.command(name="unpacked", help="Распаковка пакета")
def unpacked(
        plugin_pack: Path = typer.Argument(..., help="Путь до пакета"),
        path_output: Path = typer.Argument(..., help="Путь домашней паки Overlay")
):
    try:
        utils.unpacked(plugin_pack, path_output)
        typer.secho(f"Пакет успешно распакован", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f"Возникла ошибка: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app(help_option_names=["--help", "-h"])
