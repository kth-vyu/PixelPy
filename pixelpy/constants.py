"""
Константы для библиотеки PixelPy.
"""
from typing import Dict, List, Tuple
from PIL import Image

# Допустимые размеры сетки
VALID_GRID_SIZES = {8, 16, 32, 128}

# Значения по умолчанию
DEFAULT_GRID_SIZE = 32
DEFAULT_NUM_COLORS = 32
DEFAULT_GRID_COLOR = (0, 0, 0)
DEFAULT_SCALE_FACTOR = 20
DEFAULT_QUALITY = 95
DEFAULT_BACKGROUND_COLOR = (255, 255, 255)

# Поддерживаемые форматы файлов
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

# Настройки по умолчанию для разных форматов
FORMAT_SETTINGS: Dict[str, Dict] = {
    '.png': {'optimize': True},
    '.jpg': {'quality': DEFAULT_QUALITY, 'optimize': True},
    '.jpeg': {'quality': DEFAULT_QUALITY, 'optimize': True},
    '.bmp': {},
    '.gif': {'optimize': True}
}

# Минимальные и максимальные значения
MIN_GRID_SIZE = 8
MAX_GRID_SIZE = 128
MIN_NUM_COLORS = 2
MAX_NUM_COLORS = 256
MIN_SCALE_FACTOR = 1
MAX_SCALE_FACTOR = 100

# Предустановленные палитры
PRESET_PALETTES: Dict[str, List[Tuple[int, int, int]]] = {
    'retro': [
        (0, 0, 0), (255, 255, 255),
        (255, 0, 0), (0, 255, 0),
        (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255)
    ],
    'pastel': [
        (255, 182, 193), (176, 224, 230),
        (221, 160, 221), (176, 196, 222),
        (255, 218, 185), (230, 230, 250),
        (255, 255, 224), (240, 248, 255)
    ],
    'monochrome': [
        (0, 0, 0), (64, 64, 64),
        (128, 128, 128), (192, 192, 192),
        (255, 255, 255)
    ]
}

# Настройки алгоритмов пикселизации
PIXELIZATION_ALGORITHMS = {
    'nearest': Image.NEAREST,
    'bilinear': Image.BILINEAR,
    'bicubic': Image.BICUBIC,
    'lanczos': Image.LANCZOS
}

# Настройки палитры
PALETTE_ALGORITHMS = {
    'adaptive': Image.Quantize.MEDIANCUT,
    'web': Image.Quantize.MAXCOVERAGE
}

# Параметры пикселизации
DEFAULT_PALETTE_ALGORITHM = 'adaptive'
DEFAULT_PIXELIZATION_ALGORITHM = Image.Resampling.NEAREST

# Настройки форматов
FORMAT_SETTINGS = {
    '.png': {'format': 'PNG', 'mode': 'RGB'},
    '.jpg': {'format': 'JPEG', 'mode': 'RGB', 'quality': 95},
    '.jpeg': {'format': 'JPEG', 'mode': 'RGB', 'quality': 95},
    '.bmp': {'format': 'BMP', 'mode': 'RGB'},
    '.gif': {'format': 'GIF', 'mode': 'RGB'}
} 
