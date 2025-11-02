import subprocess
import threading
import os
import sys
import typing
from typing import Callable, Optional


def run_detached(
        command: list[str] | str,
        on_error: Optional[Callable[[int, str], None]] = None,
        on_result: Optional[Callable[[str], None]] = None
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
    return process


def check_type_simple(value: typing.Any, expected_type) -> bool:
    try:
        # Any пропускает любые значения
        if expected_type is typing.Any:
            return True
        
        # Если expected_type - строка, ищем в MRO value
        if isinstance(expected_type, str):
            # Получаем все классы из MRO
            mro_classes = value.__class__.__mro__
            
            # Ищем класс с нужным именем в MRO
            for cls in mro_classes:
                if cls.__name__ == expected_type:
                    return True
            return False
        
        # Прямая проверка для обычных типов
        if isinstance(expected_type, type):
            return isinstance(value, expected_type)
        
        # Union types
        origin = typing.get_origin(expected_type)
        if origin is typing.Union:
            return any(check_type_simple(value, t) for t in typing.get_args(expected_type))
        
        # Optional
        if origin is typing.Optional:
            return value is None or check_type_simple(value, typing.get_args(expected_type)[0])
        
        # Для остальных случаев пытаемся использовать isinstance с origin
        if origin is not None:
            return isinstance(value, origin)
        
        return False
    except (TypeError, AttributeError):
        # Если проверка не удалась, считаем что тип не совпадает
        return False