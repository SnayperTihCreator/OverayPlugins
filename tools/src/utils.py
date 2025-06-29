from wcmatch.fnmatch import fnmatch


def should_exclude(path: str, exclude_patterns: list[str]) -> bool:
    """Проверяет, нужно ли исключить файл/папку на основе паттернов"""
    for pattern in exclude_patterns:
        if fnmatch(path, pattern):
            return True
    return False
