from functools import cache


@cache
def isWayland() -> bool:
    """
    Проверяет, работает ли система под Wayland.

    :return: True если используется Wayland
    :note: Проверяет переменные окружения WAYLAND_DISPLAY и XDG_SESSION_TYPE
    """
    ...


@cache
def isProton() -> bool:
    """
    Проверяет, запущена ли программа под Proton.

    :return: True если работает под Proton
    :note: Проверяет переменные окружения Steam
    """
    ...


@cache
def getSystem() -> list[str]:
    """
    Возвращает информацию о платформе и оконной системе.

    :return: [платформа, оконная_система]
    :rtype: list[str]
    :example: ['linux', 'wayland']
    """
    ...