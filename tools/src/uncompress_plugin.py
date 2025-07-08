from pathlib import Path
from zipfile import ZipFile


def uncompress_plugin(zip_archive, output_dir):
    app_folder = Path(output_dir)
    plugin_name = Path(zip_archive).stem
    plugins_folder = app_folder/"plugins"
    tools_folder = app_folder/"tools"
    
    with ZipFile(zip_archive, "r") as zfile:
        for file in zfile.namelist():
            if file.startswith(str(tools_folder)):
                zfile.extract(file, app_folder)
        
        zfile.extract(plugin_name+".zip", plugins_folder)
        
        