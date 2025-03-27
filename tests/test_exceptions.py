"""
Тесты для пользовательских исключений библиотеки PixelPy.
"""
from typing import Dict

import pytest

from pixelpy import (
    FileOperationError,
    ImageProcessingError,
    InvalidColorError,
    InvalidGridSizeError,
    InvalidImageFormatError,
    InvalidParameterError,
    PixelPyError,
)


class TestPixelPyError:
    """Тесты базового класса исключений."""

    def test_base_error(self):
        """Тест базового исключения."""
        error = PixelPyError("Test error")
        assert str(error) == "Test error"
        assert error.details == {}

    def test_error_with_details(self):
        """Тест исключения с дополнительными деталями."""
        details = {"param": "value", "code": 123}
        error = PixelPyError("Test error", details)
        assert str(error) == "Test error"
        assert error.details == details


class TestInvalidGridSizeError:
    """Тесты исключения для некорректного размера сетки."""

    def test_invalid_grid_size(self):
        """Тест исключения с сообщением."""
        error = InvalidGridSizeError("Invalid grid size")
        assert str(error) == "Invalid grid size"
        assert isinstance(error, PixelPyError)


class TestInvalidImageFormatError:
    """Тесты исключения для неподдерживаемого формата изображения."""

    def test_invalid_format(self):
        """Тест исключения с сообщением."""
        error = InvalidImageFormatError("Invalid format")
        assert str(error) == "Invalid format"
        assert isinstance(error, PixelPyError)


class TestImageProcessingError:
    """Тесты исключения для ошибок обработки изображения."""

    def test_processing_error(self):
        """Тест исключения с сообщением."""
        error = ImageProcessingError("Processing error")
        assert str(error) == "Processing error"
        assert isinstance(error, PixelPyError)


class TestInvalidColorError:
    """Тесты исключения для некорректного цвета."""

    def test_invalid_color(self):
        """Тест исключения с сообщением."""
        error = InvalidColorError("Invalid color")
        assert str(error) == "Invalid color"
        assert isinstance(error, PixelPyError)


class TestInvalidParameterError:
    """Тесты исключения для некорректных параметров."""

    def test_invalid_parameter(self):
        """Тест исключения с сообщением."""
        error = InvalidParameterError("Invalid parameter")
        assert str(error) == "Invalid parameter"
        assert isinstance(error, PixelPyError)


class TestFileOperationError:
    """Тесты исключения для ошибок работы с файлами."""

    def test_file_error(self):
        """Тест исключения с сообщением."""
        error = FileOperationError("File error")
        assert str(error) == "File error"
        assert isinstance(error, PixelPyError)


def test_error_hierarchy():
    """Тест иерархии исключений."""
    assert issubclass(InvalidGridSizeError, PixelPyError)
    assert issubclass(InvalidImageFormatError, PixelPyError)
    assert issubclass(ImageProcessingError, PixelPyError)
    assert issubclass(InvalidColorError, PixelPyError)
    assert issubclass(InvalidParameterError, PixelPyError)
    assert issubclass(FileOperationError, PixelPyError) 