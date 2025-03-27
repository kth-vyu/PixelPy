"""
Утилиты для работы с изображениями и цветами.
"""

from typing import Dict, List, Tuple, Union
from pathlib import Path
from PIL import Image
import numpy as np

from .constants import (
    FORMAT_SETTINGS,
    MAX_NUM_COLORS,
    MAX_SCALE_FACTOR,
    MIN_NUM_COLORS,
    MIN_SCALE_FACTOR,
    PALETTE_ALGORITHMS,
    PIXELIZATION_ALGORITHMS,
    PRESET_PALETTES,
    SUPPORTED_FORMATS,
)
from .exceptions import (
    FileOperationError,
    ImageProcessingError,
    InvalidColorError,
    InvalidImageFormatError,
    InvalidParameterError,
)


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Преобразует цвет из RGB в HEX формат.

    Args:
        rgb: Кортеж с тремя целыми числами, представляющими RGB значения (0-255)

    Returns:
        Строка с HEX-представлением цвета

    Raises:
        InvalidColorError: Если значения RGB вне допустимого диапазона
    """
    if not all(0 <= x <= 255 for x in rgb):
        raise InvalidColorError("Значения RGB должны быть в диапазоне [0, 255]")
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Преобразует цвет из HEX в RGB формат.

    Args:
        hex_color: Строка с HEX-представлением цвета (например, '#FF0000')

    Returns:
        Кортеж с тремя целыми числами, представляющими RGB значения

    Raises:
        InvalidColorError: Если HEX-строка некорректна
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise InvalidColorError("HEX-строка должна содержать 6 символов")
    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise InvalidColorError("Некорректный формат HEX-строки")


def validate_image_path(path: Union[str, Path]) -> Path:
    """
    Проверяет корректность пути к изображению.

    Args:
        path: Путь к файлу изображения

    Returns:
        Path: Объект Path с путем к файлу

    Raises:
        InvalidImageFormatError: Если файл не существует или имеет неподдерживаемый формат
    """
    path = Path(path)
    if not path.exists():
        raise InvalidImageFormatError(f"Файл {path} не существует")
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise InvalidImageFormatError(
            f"Неподдерживаемый формат файла. Поддерживаемые форматы: {SUPPORTED_FORMATS}"
        )
    return path


def validate_num_colors(num_colors: int) -> None:
    """
    Проверяет корректность количества цветов.

    Args:
        num_colors: Количество цветов

    Raises:
        InvalidParameterError: Если количество цветов вне допустимого диапазона
    """
    if not MIN_NUM_COLORS <= num_colors <= MAX_NUM_COLORS:
        raise InvalidParameterError(
            f"Количество цветов должно быть в диапазоне [{MIN_NUM_COLORS}, {MAX_NUM_COLORS}]"
        )


def validate_scale_factor(scale_factor: int) -> None:
    """
    Проверяет корректность масштабного коэффициента.

    Args:
        scale_factor: Масштабный коэффициент

    Raises:
        InvalidParameterError: Если масштабный коэффициент вне допустимого диапазона
    """
    if not MIN_SCALE_FACTOR <= scale_factor <= MAX_SCALE_FACTOR:
        raise InvalidParameterError(
            f"Масштабный коэффициент должен быть в диапазоне [{MIN_SCALE_FACTOR}, {MAX_SCALE_FACTOR}]"
        )


def get_palette_from_image(image: Union[str, Path, Image.Image]) -> Dict[int, str]:
    """
    Извлекает уникальные цвета из изображения.

    Args:
        image: Путь к изображению или объект PIL.Image

    Returns:
        Словарь, где ключи - индексы цветов, значения - HEX-представление цветов

    Raises:
        ImageProcessingError: Если произошла ошибка при обработке изображения
    """
    try:
        if isinstance(image, (str, Path)):
            img = Image.open(image).convert("RGB")
        else:
            img = image.convert("RGB")

        pixels = np.array(img)
        unique_colors = np.unique(pixels.reshape(-1, 3), axis=0)
        return {i: rgb_to_hex(tuple(color)) for i, color in enumerate(unique_colors)}
    except Exception as e:
        raise ImageProcessingError(f"Ошибка при обработке изображения: {str(e)}")


def get_format_settings(format: str) -> Dict:
    """
    Возвращает настройки для указанного формата файла.

    Args:
        format: Расширение формата файла (например, '.png')

    Returns:
        Словарь с настройками для формата
    """
    return FORMAT_SETTINGS.get(format.lower(), {})


def get_preset_palette(name: str) -> List[Tuple[int, int, int]]:
    """
    Возвращает предустановленную палитру цветов.

    Args:
        name: Название палитры ('retro', 'pastel', 'monochrome')

    Returns:
        Список цветов в формате RGB

    Raises:
        InvalidParameterError: Если палитра не найдена
    """
    if name not in PRESET_PALETTES:
        raise InvalidParameterError(
            f"Палитра '{name}' не найдена. Доступные палитры: {list(PRESET_PALETTES.keys())}"
        )
    return PRESET_PALETTES[name]


def get_pixelization_algorithm(name: str) -> int:
    """
    Возвращает алгоритм пикселизации.

    Args:
        name: Название алгоритма ('nearest', 'bilinear', 'bicubic', 'lanczos')

    Returns:
        Константа алгоритма из PIL

    Raises:
        InvalidParameterError: Если алгоритм не найден
    """
    if name not in PIXELIZATION_ALGORITHMS:
        raise InvalidParameterError(
            f"Алгоритм '{name}' не найден. Доступные алгоритмы: {list(PIXELIZATION_ALGORITHMS.keys())}"
        )
    return PIXELIZATION_ALGORITHMS[name]


def get_palette_algorithm(name: str) -> int:
    """
    Возвращает алгоритм создания палитры.

    Args:
        name: Название алгоритма ('adaptive', 'web')

    Returns:
        Константа алгоритма из PIL

    Raises:
        InvalidParameterError: Если алгоритм не найден
    """
    if name not in PALETTE_ALGORITHMS:
        raise InvalidParameterError(
            f"Алгоритм '{name}' не найден. Доступные алгоритмы: {list(PALETTE_ALGORITHMS.keys())}"
        )
    return PALETTE_ALGORITHMS[name]


def save_image(image: Image.Image, path: Union[str, Path], **kwargs) -> None:
    """
    Сохраняет изображение с учетом формата и настроек.

    Args:
        image: Объект PIL.Image
        path: Путь для сохранения
        **kwargs: Дополнительные параметры сохранения

    Raises:
        FileOperationError: Если произошла ошибка при сохранении
    """
    try:
        path = Path(path)
        format_settings = get_format_settings(path.suffix)
        format_settings.update(kwargs)
        image.save(path, **format_settings)
    except Exception as e:
        raise FileOperationError(f"Ошибка при сохранении изображения: {str(e)}")
