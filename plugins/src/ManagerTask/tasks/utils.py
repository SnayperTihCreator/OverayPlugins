import subprocess
import threading
import atexit
import os
import sys
import signal
from typing import Callable, Optional


def run_detached(
        command: list[str] | str,
        on_error: Optional[Callable[[int, str], None]] = None,
        on_result: Optional[Callable[[str], None]] = None,
        on_close: bool = True
) -> subprocess.Popen:
    """
    Запускает команду в фоне, убивает при выходе родителя и вызывает callback при ошибке.

    Args:
        command (list): Команда для запуска (например, ["python", "script.py"]).
        on_error (callback): Функция, которая получит (returncode, stderr) при ошибке.
        on_result (callback): Функция, которая получит (stdout) при завершении.

    Returns:
        subprocess.Popen: Объект процесса (если нужно вручную управлять).
    """
    kwargs = {
        'stdout': subprocess.PIPE,  # Перенаправляем вывод для анализа
        'stderr': subprocess.PIPE,
    }
    
    # Платформозависимые флаги
    if sys.platform == 'win32':
        kwargs['creationflags'] = (
                subprocess.CREATE_NEW_PROCESS_GROUP |
                subprocess.DETACHED_PROCESS
        )
    else:
        kwargs['preexec_fn'] = os.setsid  # Новая группа процессов (Linux/macOS)
    
    process = subprocess.Popen(command, **kwargs)
    
    def monitor_process():
        """Мониторит процесс и вызывает callback при ошибке."""
        stdout, stderr = process.communicate()  # Ждём завершения
        if process.returncode != 0 and on_error:  # Если была ошибка
            error_msg = stderr if stderr else ""
            on_error(process.returncode, error_msg)
        if process.returncode == 0 and on_result:
            result_msg = stdout if stdout else ""
            on_result(result_msg)
    
    threading.Thread(target=monitor_process, daemon=True).start()
    
    def cleanup():
        """Убивает дочерний процесс при выходе родителя."""
        if process.poll() is None:  # Если ещё работает
            if sys.platform == 'win32':
                process.terminate()  # SIGTERM
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Убиваем группу
            process.wait()  # Ожидаем завершения (опционально)
    
    if on_close:
        atexit.register(cleanup)  # Гарантированное завершение
    return process
