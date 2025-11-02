import subprocess

# Использование start /B
subprocess.Popen(["python", "utils.py"])
print("Команда запущена в фоне - можно продолжать")