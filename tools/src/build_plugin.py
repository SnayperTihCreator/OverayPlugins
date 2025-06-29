import zipfile
from pathlib import Path, PurePath

from utils import should_exclude


def build_plugin(path, exclude_patterns, output_dir):
    plugin_name = Path(path).name
    path = Path(path)
    zip_filename = Path(output_dir) / f"{plugin_name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in path.rglob("*"):
            
            if should_exclude(str(file), exclude_patterns): continue
            if not file.is_file(): continue
            
            if file.suffix == ".py":
                file_push = plugin_name/file.relative_to(*file.parts[:file.parts.index(plugin_name) + 1])
            else:
                file_push = file.relative_to(*file.parts[:file.parts.index(plugin_name) + 1])
            
            zipf.write(file, file_push)
    
    return zip_filename.name
