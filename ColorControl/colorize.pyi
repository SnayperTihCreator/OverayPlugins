from PySide6.QtGui import QIcon, QPixmap, QImage, QColor


def modulateIcon(icon: QIcon, color: QColor) -> QIcon:
    """
    Тонирует иконку указанным цветом с сохранением альфа-канала.

    :param QIcon icon: Исходная иконка для тонирования
    :param QColor color: Цвет для наложения
    :return QIcon: Новая тонированная иконка.
    :note: Возвращает исходную иконку если цвет невалиден или иконка пуста
    """
    ...


def modulatePixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
    """
    Тонирует пиксмап указанным цветом с сохранением альфа-канала.

    :param QPixmap pixmap: Исходное изображение
    :param QColor color: Цвет для наложения
    :return QPixmap: Новый тонированный пиксмап.
    :note: Возвращает исходный пиксмап если цвет невалиден или изображение пусто
    """
    ...


def modulateImage(image: QImage, color: QColor) -> QImage:
    """
    Тонирует изображение указанным цветом с сохранением альфа-канала.

    :param QImage image: Исходное изображение
    :param QColor color: Цвет для наложения
    :return QImage: Новое тонированное изображение.
    :note: Возвращает исходное изображение если цвет невалиден или изображение пусто.
    :note: Использует формат ARGB32 для выходного изображения
    """
    ...


__all__ = ["modulateIcon", "modulateImage", "modulatePixmap"]