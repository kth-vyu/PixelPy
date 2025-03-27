"""
PixelPy - библиотека для создания пиксельных изображений.
"""

from .exceptions import (
    FileOperationError,
    ImageProcessingError,
    InvalidColorError,
    InvalidGridSizeError,
    InvalidImageFormatError,
    InvalidParameterError,
    PixelPyError,
)
from .pixelizer import Pixelizer
from .utils import (
    get_format_settings,
    get_palette_algorithm,
    get_palette_from_image,
    get_pixelization_algorithm,
    get_preset_palette,
    hex_to_rgb,
    rgb_to_hex,
)

__version__ = "0.1.0"
__author__ = "kth.vyu"
__email__ = "kozyreva.k1@ya.ru"

__all__ = [
    # Основные классы
    "Pixelizer",
    # Утилиты
    "get_palette_from_image",
    "get_format_settings",
    "get_preset_palette",
    "get_pixelization_algorithm",
    "get_palette_algorithm",
    "rgb_to_hex",
    "hex_to_rgb",
    # Исключения
    "PixelPyError",
    "InvalidGridSizeError",
    "InvalidImageFormatError",
    "ImageProcessingError",
    "InvalidColorError",
    "InvalidParameterError",
    "FileOperationError",
]
