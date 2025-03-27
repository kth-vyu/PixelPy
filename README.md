# PixelPy

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

PixelPy - это современная Python библиотека для создания пиксельных изображений с настраиваемой сеткой и цветовой палитрой. Библиотека предоставляет простой и эффективный способ преобразования изображений в пиксельное искусство.

## Особенности

- 🎨 Создание пиксельных изображений с настраиваемой сеткой
- 🎯 Поддержка различных размеров сетки (8x8, 16x16, 32x32, 128x128)
- 🎨 Настраиваемая цветовая палитра
- 📏 Автоматическое преобразование в квадратное изображение
- 🖼️ Сохранение палитры цветов
- 🎨 Настраиваемый цвет сетки
- 🔍 Валидация входных данных
- 🛠️ Модульная архитектура

## Установка

```bash
pip install pixelpy
```

## Быстрый старт

```python
from pixelpy import Pixelizer

# Создание экземпляра пикселизатора с настройками по умолчанию
pixelizer = Pixelizer()

# Базовое использование
pixelizer.pixelize(
    image_path="input.jpg",
    output_path="output.png"
)

# Создание пикселизатора с пользовательскими настройками
custom_pixelizer = Pixelizer(
    grid_size=16,
    grid_color=(255, 0, 0),  # Красная сетка
    num_colors=16,
    scale_factor=30
)

# Использование пользовательских настроек
custom_pixelizer.pixelize(
    image_path="input.jpg",
    output_path="output_custom.png"
)

# Получение палитры цветов
from pixelpy import get_palette_from_image
palette = get_palette_from_image("output.png")
```

## API

### Pixelizer

Основной класс для пикселизации изображений.

```python
class Pixelizer(
    grid_size: int = 32,
    grid_color: Tuple[int, int, int] = (0, 0, 0),
    num_colors: int = 32,
    scale_factor: int = 20
)
```

#### Параметры конструктора

- `grid_size`: Размер сетки (8, 16, 32, 128)
- `grid_color`: Цвет сетки в формате RGB
- `num_colors`: Количество цветов в палитре
- `scale_factor`: Масштабный коэффициент для увеличения размера пикселей

#### Методы

##### pixelize

```python
def pixelize(
    self,
    image_path: Union[str, Path],
    output_path: Union[str, Path],
) -> Dict[int, str]
```

Преобразует изображение в пиксельное с указанными параметрами.

**Параметры:**
- `image_path`: Путь к входному файлу изображения
- `output_path`: Путь для сохранения выходного файла

**Возвращает:**
- Словарь с палитрой цветов, где ключи - индексы цветов, значения - HEX-представление цветов

### Утилиты

#### get_palette_from_image

```python
def get_palette_from_image(image: Union[str, Path, Image.Image]) -> Dict[int, str]
```

Извлекает уникальные цвета из изображения.

**Параметры:**
- `image`: Путь к изображению или объект PIL.Image

**Возвращает:**
- Словарь с палитрой цветов

## Поддерживаемые форматы

- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)

## Требования

- Python >= 3.11
- Pillow >= 9.0.0
- numpy >= 1.21.0

## Лицензия

MIT License - см. [LICENSE](LICENSE) для подробностей.