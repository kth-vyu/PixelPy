"""
Тесты для основного класса Pixelizer.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

import pytest
from PIL import Image

from pixelpy import (
    FileOperationError,
    ImageProcessingError,
    InvalidColorError,
    InvalidGridSizeError,
    InvalidImageFormatError,
    InvalidParameterError,
    Pixelizer,
    get_palette_from_image,
    rgb_to_hex,
)

# Пути к тестовым изображениям
TEST_IMAGES_DIR = Path(__file__).parent / "test_images"
INPUT_IMAGE = TEST_IMAGES_DIR / "input.jpg"
OUTPUT_DIR = TEST_IMAGES_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


@pytest.fixture
def pixelizer():
    """Фикстура для создания базового экземпляра Pixelizer."""
    return Pixelizer()


@pytest.fixture
def custom_pixelizer():
    """Фикстура для создания экземпляра Pixelizer с пользовательскими настройками."""
    return Pixelizer(
        grid_size=16,
        grid_color=(255, 0, 0),
        num_colors=16,
        scale_factor=30,
        background_color=(255, 255, 255),
        pixelization_algorithm="lanczos",
        palette_algorithm="web",
    )


class TestPixelizerInitialization:
    """Тесты инициализации класса Pixelizer."""

    def test_default_initialization(self):
        """Тест инициализации с параметрами по умолчанию."""
        pixelizer = Pixelizer()
        assert pixelizer.grid_size == 32
        assert pixelizer.grid_color == (0, 0, 0)
        assert pixelizer.num_colors == 32
        assert pixelizer.scale_factor == 20
        assert pixelizer.background_color == (255, 255, 255)

    def test_custom_initialization(self):
        """Тест инициализации с пользовательскими параметрами."""
        pixelizer = Pixelizer(
            grid_size=16,
            grid_color=(255, 0, 0),
            num_colors=16,
            scale_factor=30,
            background_color=(0, 0, 0),
        )
        assert pixelizer.grid_size == 16
        assert pixelizer.grid_color == (255, 0, 0)
        assert pixelizer.num_colors == 16
        assert pixelizer.scale_factor == 30
        assert pixelizer.background_color == (0, 0, 0)

    def test_invalid_grid_size(self):
        """Тест инициализации с некорректным размером сетки."""
        with pytest.raises(InvalidGridSizeError):
            Pixelizer(grid_size=64)

    def test_invalid_num_colors(self):
        """Тест инициализации с некорректным количеством цветов."""
        with pytest.raises(InvalidParameterError):
            Pixelizer(num_colors=1)

    def test_invalid_scale_factor(self):
        """Тест инициализации с некорректным масштабным коэффициентом."""
        with pytest.raises(InvalidParameterError):
            Pixelizer(scale_factor=0)


class TestPixelizerBasicOperations:
    """Тесты базовых операций класса Pixelizer."""

    def test_basic_pixelization(self, pixelizer, input_image, output_dir):
        """Тест базовой пикселизации."""
        output_path = output_dir / "basic_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert isinstance(palette, dict)
        assert all(isinstance(color, str) for color in palette.values())
        assert all(color.startswith("#") for color in palette.values())

    def test_custom_pixelization(self, custom_pixelizer, input_image, output_dir):
        """Тест пикселизации с пользовательскими настройками."""
        output_path = output_dir / "custom_output.png"
        palette = custom_pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert isinstance(palette, dict)
        assert len(palette) <= custom_pixelizer.num_colors

    def test_invalid_input_path(self, pixelizer, output_dir):
        """Тест обработки некорректного пути к входному файлу."""
        with pytest.raises(InvalidImageFormatError):
            pixelizer.pixelize("nonexistent.jpg", output_dir / "error.png")

    def test_invalid_output_format(self, pixelizer, input_image, output_dir):
        """Тест обработки неподдерживаемого формата выходного файла."""
        with pytest.raises(InvalidImageFormatError):
            pixelizer.pixelize(input_image, output_dir / "output.txt")


class TestPixelizerPalettes:
    """Тесты работы с палитрами."""

    def test_preset_palettes(self, pixelizer, input_image, output_dir):
        """Тест использования предустановленных палитр."""
        palettes = ["retro", "pastel", "monochrome"]
        for palette_name in palettes:
            output_path = output_dir / f"palette_{palette_name}.png"
            palette = pixelizer.pixelize(
                input_image, output_path, preset_palette=palette_name
            )

            assert output_path.exists()
            assert isinstance(palette, dict)
            assert len(palette) <= pixelizer.num_colors

    def test_custom_palette(self, input_image, output_dir):
        """Тест использования пользовательской палитры."""
        custom_palette = [
            (0, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
        ]
        pixelizer = Pixelizer(custom_palette=custom_palette)
        output_path = output_dir / "custom_palette_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert len(palette) <= len(custom_palette)


class TestPixelizerAlgorithms:
    """Тесты различных алгоритмов обработки."""

    def test_pixelization_algorithms(self, input_image, output_dir):
        """Тест различных алгоритмов пикселизации."""
        algorithms = ["nearest", "bilinear", "bicubic", "lanczos"]
        for algorithm in algorithms:
            pixelizer = Pixelizer(pixelization_algorithm=algorithm)
            output_path = output_dir / f"algorithm_{algorithm}.png"
            palette = pixelizer.pixelize(input_image, output_path)

            assert output_path.exists()
            assert isinstance(palette, dict)

    def test_palette_algorithms(self, input_image, output_dir):
        """Тест различных алгоритмов создания палитры."""
        algorithms = ["adaptive", "web"]
        for algorithm in algorithms:
            pixelizer = Pixelizer(palette_algorithm=algorithm)
            output_path = output_dir / f"palette_algorithm_{algorithm}.png"
            palette = pixelizer.pixelize(input_image, output_path)

            assert output_path.exists()
            assert isinstance(palette, dict)


class TestPixelizerEdgeCases:
    """Тесты граничных случаев."""

    def test_minimum_grid_size(self, input_image, output_dir):
        """Тест минимального размера сетки."""
        pixelizer = Pixelizer(grid_size=8)
        output_path = output_dir / "min_grid_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert isinstance(palette, dict)

    def test_maximum_grid_size(self, input_image, output_dir):
        """Тест максимального размера сетки."""
        pixelizer = Pixelizer(grid_size=128)
        output_path = output_dir / "max_grid_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert isinstance(palette, dict)

    def test_minimum_colors(self, input_image, output_dir):
        """Тест минимального количества цветов."""
        pixelizer = Pixelizer(num_colors=2)
        output_path = output_dir / "min_colors_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert len(palette) <= 2

    def test_maximum_colors(self, input_image, output_dir):
        """Тест максимального количества цветов."""
        pixelizer = Pixelizer(num_colors=256)
        output_path = output_dir / "max_colors_output.png"
        palette = pixelizer.pixelize(input_image, output_path)

        assert output_path.exists()
        assert len(palette) <= 256


class TestPixelizerImageProcessing:
    """Тесты обработки изображений."""

    def test_square_image(self, pixelizer, input_image, output_dir):
        """Тест обработки квадратного изображения."""
        output_path = output_dir / "square_output.png"
        pixelizer.pixelize(input_image, output_path)

        img = Image.open(output_path)
        assert img.size[0] == img.size[1]
        assert img.size[0] == pixelizer.grid_size * pixelizer.scale_factor

    def test_background_color(self, input_image, output_dir):
        """Тест применения цвета фона."""
        pixelizer = Pixelizer(background_color=(0, 0, 0))
        output_path = output_dir / "background_output.png"
        pixelizer.pixelize(input_image, output_path)

        img = Image.open(output_path)
        assert img.getpixel((0, 0)) == (0, 0, 0)

    def test_grid_color(self, input_image, output_dir):
        """Тест применения цвета сетки."""
        grid_color = (255, 0, 0)
        pixelizer = Pixelizer(grid_color=grid_color)
        output_path = output_dir / "grid_color_output.png"
        pixelizer.pixelize(input_image, output_path)

        img = Image.open(output_path)
        assert img.getpixel((pixelizer.scale_factor, 0)) == grid_color


class TestPixelizerUtils:
    """Тесты утилитарных функций."""

    def test_rgb_to_hex(self):
        """Тест конвертации RGB в HEX."""
        assert rgb_to_hex((255, 0, 0)) == "#ff0000"
        assert rgb_to_hex((0, 255, 0)) == "#00ff00"
        assert rgb_to_hex((0, 0, 255)) == "#0000ff"

    def test_invalid_rgb(self):
        """Тест обработки некорректных RGB значений."""
        with pytest.raises(InvalidColorError):
            rgb_to_hex((-1, 0, 0))
        with pytest.raises(InvalidColorError):
            rgb_to_hex((0, 256, 0))

    def test_get_palette_from_image(self, input_image):
        """Тест извлечения палитры из изображения."""
        palette = get_palette_from_image(input_image)
        assert isinstance(palette, dict)
        assert all(isinstance(color, str) for color in palette.values())
        assert all(color.startswith("#") for color in palette.values())
