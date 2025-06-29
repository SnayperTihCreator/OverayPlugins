import typer
import zipfile
import os
import re
from pathlib import Path
import toml
from typing import List, Optional

app = typer.Typer()


from build_plugin import build_plugin
@app.command()
def BuildPlugin(
        plugin_name_or_toml: str = typer.Argument(..., help="Имя плагина или путь к TOML файлу"),
        exclude: Optional[List[str]] = typer.Option(
            None,
            help="Регулярные выражения для исключения файлов/папок"
        ),
        output_dir: str = typer.Option(
            ".",
            help="Директория для сохранения zip-файла"
        )
):
    """
    Создает zip-архив плагина:
    - Все .py файлы помещаются в подпапку с именем плагина
    - Остальные файлы помещаются в корень архива
    - Поддерживает исключения через регулярные выражения
    - Поддерживает конфигурацию через TOML файл
    """
    # Обработка конфигурации из TOML
    if plugin_name_or_toml.endswith('.toml') and os.path.exists(plugin_name_or_toml):
        with open(plugin_name_or_toml, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        plugin_name = config.get('plugin', {}).get('path', '.')
        exclude_patterns = config.get('build', {}).get('exclude', [])
        if exclude:
            exclude_patterns.extend(exclude)
    else:
        plugin_name = plugin_name_or_toml
        exclude_patterns = exclude or []
    
    exclude_patterns += ["*/__pycache__/*", "*/.git/*", "*/temp/*", "*.tmp"]
        
    zip_filename = build_plugin(plugin_name, exclude_patterns, output_dir)
    
    typer.echo(f"Плагин {plugin_name} успешно собран в {zip_filename}")


@app.command()
def passed():
    pass

if __name__ == "__main__":
    app()
