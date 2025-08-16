import fs
from typing import Optional, Callable, Set, Tuple
from jinja2 import BaseLoader, Environment


class FSLoader(BaseLoader):
    """
    Загрузчик шаблонов Jinja2 из файловой системы (fs).

    Наследуется от BaseLoader и реализует загрузку шаблонов
    через библиотеку PyFilesystem (fs).
    """

    def __init__(
        self,
        template_fs: str,
        encoding: str = 'utf-8',
        use_syspath: bool = False,
        fs_filter: Optional[Callable] = None
    ) -> None:
        """
        Инициализирует загрузчик шаблонов.

        :param template_fs: Путь к файловой системе или URL
        :param encoding: Кодировка файлов (по умолчанию utf-8)
        :param use_syspath: Использовать системные пути если доступны
        :param fs_filter: Фильтр для поиска файлов
        """
        self.filesystem: fs.base.FS = ...
        self.use_syspath: bool = ...
        self.encoding: str = ...
        self.fs_filter: Optional[Callable] = ...
        ...

    def get_source(
        self,
        environment: Environment,
        template: str
    ) -> Tuple[str, str, Callable[[], bool]]:
        """
        Загружает исходный код шаблона.

        :param environment: Окружение Jinja2
        :param template: Имя шаблона
        :return: Кортеж (source, path, reload_func)
        :raises TemplateNotFound: Если шаблон не найден
        :note: reload_func всегда возвращает False
        """
        ...

    def list_templates(self) -> Set[str]:
        """
        Возвращает список доступных шаблонов.

        :return: Множество относительных путей к шаблонам
        :note: Результат сортируется в алфавитном порядке
        """
        ...