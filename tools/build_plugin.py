import os
import toml
import zipfile
import io
from pathlib import Path
from fnmatch import fnmatch


class PluginPackager:
    def __init__(self, config_file: str = 'collected.toml'):
        self.config_file = config_file
        self.config = self._load_config()
        
        self.plugin_name = self.config['plugin']['name']
        self.tools_dir = self.config.get('settings', {}).get('tools_dir', 'tools')
        
        # Настройки исключений
        self.exclude_dirs = set(self.config.get('exclude', {}).get('dirs', ['__pycache__']))
        self.exclude_files = set(self.config.get('exclude', {}).get('files', ['.*']))
        self.plugin_dirs_excludes = set(self.config.get('exclude', {}).get('plugin_dirs', []))
        self.plugin_files_excludes = set(self.config.get('exclude', {}).get('plugin_files', []))
    
    def _load_config(self) -> dict:
        """Загружает конфигурационный файл"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return toml.load(f)
    
    def _scan_python_items(self, base_path: str, subdir:str) -> tuple[list[str], list[str]]:
        """
        Сканирует Python модули и пакеты
        Возвращает: (отдельные_модули, пакеты)
        """
        directory = Path(base_path)/subdir
        
        if not directory.exists():
            return [], []
        
        base_path = Path(base_path)
        single_modules = []
        packages = []
        processed_packages = set()
        
        for item in Path(directory).iterdir():
            # Пропускаем исключенные элементы
            if any(part.startswith('.') for part in item.parts):
                continue
            if item.name in self.exclude_dirs and item.is_dir():
                continue
            if item.is_file() and any(fnmatch(item.name, exc) for exc in self.exclude_files):
                continue
            
            # Обрабатываем пакеты (папки с __init__.py)
            if item.is_dir() and (item / '__init__.py').exists():
                rel_path = item.relative_to(base_path)
                package_name = str(rel_path).replace(os.sep, '.')
                packages.append(package_name.replace(f"{subdir}.", "", 1))
                processed_packages.add(item)
                continue
            # Обрабатываем отдельные модули (только если не в пакете)
            if item.is_file() and item.suffix == '.py':
                # Проверяем, что модуль не внутри уже обработанного пакета
                in_package = False
                for pkg_path in processed_packages:
                    if item.is_relative_to(pkg_path):
                        in_package = True
                        break
                
                if not in_package:
                    rel_path = item.relative_to(base_path)
                    module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
                    single_modules.append(module_name.lstrip(f"{subdir}."))
        
        return single_modules, packages
    
    def _create_plugin_toml(self) -> str:
        """Создает plugin.toml в памяти"""
        tools_data = {}
        for subdir in ['common', 'linux', 'windows']:
            modules, packages = self._scan_python_items(self.tools_dir, subdir)
            
            if modules or packages:
                tools_data[subdir] = {
                    'modules': modules,
                    'packages': packages
                }
        
        plugin_data = {
            'plugin': {
                'name': self.plugin_name,
                'version': self.config['plugin'].get('version', '0.1.0'),
                'author': self.config['plugin'].get('author', ''),
                'description': self.config['plugin'].get('description', ''),
            },
            'tools': tools_data
        }
        
        with io.StringIO() as f:
            toml.dump(plugin_data, f)
            return f.getvalue()
    
    def _add_directory_to_zip(self, zipf: zipfile.ZipFile, directory: str | Path):
        """Рекурсивно добавляет директорию в архив, исключая папки и файлы по маскам."""
        directory = Path(directory)
        
        # Проверяем, не нужно ли пропустить папку (по exact match или маске)
        dir_name = directory.name
        if (dir_name in self.exclude_dirs or
                any(fnmatch(dir_name, pattern) for pattern in self.plugin_dirs_excludes)):
            return
        
        for item in directory.iterdir():
            if item.is_dir():
                # Рекурсивный вызов для подпапок
                self._add_directory_to_zip(zipf, item)
            else:
                # Проверяем, не нужно ли исключить файл (по exact match или маске)
                file_name = item.name
                if (
                        file_name in self.exclude_files
                        or any(fnmatch(file_name, pattern) for pattern in self.plugin_files_excludes)
                        or any(file_name.startswith(prefix) for prefix in self.exclude_files)
                ):
                    continue
                
                # Добавляем файл в архив
                arcname = str(item.relative_to('.'))
                zipf.write(item, arcname)
    
    def create_plugin(self) -> str:
        """Создает архив плагина"""
        archive_name = f"{self.plugin_name}.plugin"
        
        if not os.path.exists(self.plugin_name):
            raise FileNotFoundError(f"Plugin directory '{self.plugin_name}' not found")
        
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем plugin.toml
            plugin_toml_content = self._create_plugin_toml()
            zipf.writestr('plugin.toml', plugin_toml_content)
            
            # Добавляем папку плагина
            self._add_directory_to_zip(zipf, self.plugin_name)
            
            # Добавляем папку tools
            if os.path.exists(self.tools_dir):
                self._add_directory_to_zip(zipf, self.tools_dir)
        
        return archive_name


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Package Python plugin')
    parser.add_argument('--config', type=str, default='collected.toml',
                        help='Configuration file (default: collected.toml)')
    
    args = parser.parse_args()
    
    try:
        packager = PluginPackager(config_file=args.config)
        archive_path = packager.create_plugin()
        print(f"Plugin created: {archive_path}")
    except Exception as e:
        print(f"Error creating plugin: {e}")
        exit(1)
