import os
import subprocess
import sys
from pathlib import Path


def run_uv_setups(target_dir="src"):
    root = Path.cwd()
    search_path = root / target_dir
    
    if not search_path.exists():
        print(f"❌ Ошибка: Папка '{target_dir}' не найдена.")
        return
    
    files = sorted(list(search_path.glob("*/setup.py")))
    if not files:
        print(f"🔍 В '{target_dir}' не найдено setup.py")
        return
    
    results = []  # Список для хранения статусов
    
    for setup_file in files:
        project_name = setup_file.parent.name
        print(f"\n{'=' * 60}")
        print(f"🚀 ЗАПУСК: {project_name}")
        print(f"{'=' * 60}")
        
        try:
            # Запускаем uv run python
            subprocess.run(
                ["uv", "run", "python", str(setup_file)],
                check=True,
                shell=(os.name == 'nt')
            )
            results.append((project_name, "✅ SUCCESS"))
        except subprocess.CalledProcessError:
            results.append((project_name, "❌ FAILED"))
        except Exception as e:
            results.append((project_name, f"⚠️ ERROR: {e}"))
    
    # ФИНАЛЬНЫЙ ОТЧЕТ
    print(f"\n\n{'=' * 25} ИТОГ СБОРКИ {'=' * 25}")
    for name, status in results:
        # Форматируем вывод в колонки
        print(f"{name:<30} {status}")
    print(f"{'=' * 62}")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "src"
    run_uv_setups(folder)