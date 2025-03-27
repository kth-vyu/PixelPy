"""
Пользовательские исключения для библиотеки PixelPy.
"""

from typing import Any, Dict, Optional


class PixelPyError(Exception):
    """Базовый класс для всех исключений PixelPy."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Инициализация исключения.

        Args:
            message: Сообщение об ошибке
            details: Дополнительные детали ошибки
        """
        super().__init__(message)
        self.details = details or {}


class InvalidGridSizeError(PixelPyError):
    """Исключение для некорректного размера сетки."""

    pass


class InvalidImageFormatError(PixelPyError):
    """Исключение для неподдерживаемого формата изображения."""

    pass


class ImageProcessingError(PixelPyError):
    """Исключение для ошибок обработки изображения."""

    pass


class InvalidColorError(PixelPyError):
    """Исключение для некорректного цвета."""

    pass


class InvalidParameterError(PixelPyError):
    """Исключение для некорректных параметров."""

    pass


class FileOperationError(PixelPyError):
    """Исключение для ошибок работы с файлами."""

    pass
