from typing import Any
from API.config import Config


def load(path: str, config: Config) -> Any:
    """
    Загружает данные плагина из YAML-файла.

    :param str path: Относительный путь к файлу данных
    :param Config config: Конфигурация плагина
    :return Any: Загруженные данные
    :raises IOError: Если файл не существует или недоступен
    :raises yaml.YAMLError: При ошибках парсинга YAML
    """
    ...


def save(path: str, config: Config, data: Any) -> None:
    """
    Сохраняет данные плагина в YAML-файл.

    :param str path: Относительный путь к файлу
    :param Config config: Конфигурация плагина
    :param Any data: Данные для сохранения
    :raises IOError: При проблемах с записью файла
    :raises yaml.YAMLError: При ошибках сериализации.
    :note: Автоматически создает директории при необходимости
    """
    ...