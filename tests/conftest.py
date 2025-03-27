"""
Конфигурация тестов для библиотеки PixelPy.
"""
import os
import shutil
from pathlib import Path

import pytest
from PIL import Image, ImageDraw


@pytest.fixture(scope="session")
def test_images_dir():
    """Фикстура для создания директории с тестовыми изображениями."""
    test_dir = Path(__file__).parent / "test_images"
    output_dir = test_dir / "output"
    
    # Создаем директории
    test_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Создаем тестовое изображение, если оно не существует
    input_image = test_dir / "input.jpg"
    if not input_image.exists():
        # Создаем тестовое изображение с градиентом и фигурами
        img = Image.new('RGB', (200, 200))
        draw = ImageDraw.Draw(img)
        
        # Рисуем градиентный фон
        for y in range(img.height):
            for x in range(img.width):
                r = int(255 * (x / img.width))
                g = int(255 * (y / img.height))
                b = int(255 * ((x + y) / (img.width + img.height)))
                draw.point((x, y), fill=(r, g, b))
        
        # Рисуем фигуры
        draw.rectangle([50, 50, 150, 150], fill=(255, 0, 0))  # Красный квадрат
        draw.ellipse([75, 75, 125, 125], fill=(0, 255, 0))   # Зеленый круг
        draw.polygon([(100, 50), (150, 100), (50, 100)], fill=(0, 0, 255))  # Синий треугольник
        
        # Сохраняем изображение
        img.save(input_image, quality=95)
    
    yield test_dir
    
    # Очищаем выходную директорию после тестов
    if output_dir.exists():
        shutil.rmtree(output_dir)
        output_dir.mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def input_image(test_images_dir):
    """Фикстура для пути к входному изображению."""
    return test_images_dir / "input.jpg"


@pytest.fixture(scope="session")
def output_dir(test_images_dir):
    """Фикстура для пути к директории с выходными файлами."""
    return test_images_dir / "output" 
