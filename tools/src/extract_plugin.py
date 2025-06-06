import os
import zipfile


class PluginExtractor:
    def __init__(self, archive_path: str, extract_to: str):
        self.archive_path = archive_path
        self.extract_to = extract_to
        self.plugins_dir = os.path.join(extract_to, 'plugins')
        self.tools_dir = os.path.join(extract_to, 'tools')
    
    def _get_plugin_name(self, archive) -> str:
        """Получаем имя плагина из plugin.toml в архиве"""
        with archive.open('plugin.toml') as f:
            content = f.read().decode('utf-8')
            # Простейший парсинг имени плагина без полного разбора TOML
            for line in content.split('\n'):
                if 'name =' in line:
                    return line.split('=')[1].strip().strip('"\'')
        return 'unknown_plugin'
    
    def extract(self):
        """Извлекает плагин из архива"""
        if not os.path.exists(self.archive_path):
            raise FileNotFoundError(f"Архив {self.archive_path} не найден")
        
        with zipfile.ZipFile(self.archive_path, 'r') as archive:
            # 1. Получаем имя плагина
            plugin_name = self._get_plugin_name(archive)
            plugin_dir = os.path.join(self.plugins_dir, plugin_name)
            
            # Создаем необходимые директории
            os.makedirs(self.tools_dir, exist_ok=True)
            
            # 2. Извлекаем файлы
            for file_info in archive.infolist():
                file_path = file_info.filename
                
                # Извлекаем plugin.toml в папку плагина
                if file_path == 'plugin.toml':
                    archive.extract(file_info, plugin_dir)
                    continue
                
                # Извлекаем содержимое tools/ в tools_dir
                if file_path.startswith('tools/'):
                    target_path = file_path
                    # Для директорий просто создаем структуру
                    if file_path.endswith('/'):
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        archive.extract(file_info, self.extract_to)
                    continue
                
                # Извлекаем остальные файлы в папку плагина (кроме plugin.toml)
                if not file_path.startswith('tools/') and file_path != 'plugin.toml':
                    target_path = file_path
                    # Для директорий
                    if file_path.endswith('/'):
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        archive.extract(file_info, self.plugins_dir)
        
        print(f"Плагин {plugin_name} успешно извлечен в {self.extract_to}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract plugin from archive')
    parser.add_argument('archive', help='Path to plugin archive (.plugin file)')
    parser.add_argument('--output', '-o', default='.',
                        help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    try:
        extractor = PluginExtractor(args.archive, args.output)
        extractor.extract()
    except Exception as e:
        print(f"Ошибка при извлечении плагина: {e}")
        exit(1)