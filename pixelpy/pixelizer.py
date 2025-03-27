"""
Основной класс для пикселизации изображений.
"""
import os
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from PIL import Image, ImageDraw

from .constants import (
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_GRID_COLOR,
    DEFAULT_GRID_SIZE,
    DEFAULT_NUM_COLORS,
    DEFAULT_SCALE_FACTOR,
    VALID_GRID_SIZES,
    DEFAULT_PALETTE_ALGORITHM,
    DEFAULT_PIXELIZATION_ALGORITHM,
    SUPPORTED_FORMATS,
    PALETTE_ALGORITHMS,
    MIN_NUM_COLORS,
    MAX_NUM_COLORS,
    MIN_SCALE_FACTOR,
    MAX_SCALE_FACTOR,
)
from .exceptions import (
    FileOperationError,
    ImageProcessingError,
    InvalidColorError,
    InvalidGridSizeError,
    InvalidImageFormatError,
    InvalidParameterError,
)
from .utils import (
    get_format_settings,
    get_palette_from_image,
    get_preset_palette,
    save_image,
    validate_image_path,
)


class Pixelizer:
    """
    Класс для преобразования изображений в пиксельное искусство.
    """

    def __init__(
        self,
        grid_size: int = DEFAULT_GRID_SIZE,
        grid_color: Tuple[int, int, int] = DEFAULT_GRID_COLOR,
        num_colors: int = DEFAULT_NUM_COLORS,
        scale_factor: int = DEFAULT_SCALE_FACTOR,
        background_color: Optional[Tuple[int, int, int]] = None,
        pixelization_algorithm: str = 'nearest',
        palette_algorithm: str = DEFAULT_PALETTE_ALGORITHM,
        custom_palette: Optional[List[Tuple[int, int, int]]] = None,
    ):
        """
        Инициализация пикселизатора.

        Args:
            grid_size: Размер сетки (8, 16, 32, 128)
            grid_color: Цвет сетки в формате RGB
            num_colors: Количество цветов в палитре
            scale_factor: Масштабный коэффициент для увеличения размера пикселей
            background_color: Цвет фона (если None, используется прозрачный)
            pixelization_algorithm: Алгоритм пикселизации ('nearest', 'bilinear', 'bicubic', 'lanczos')
            palette_algorithm: Алгоритм создания палитры ('adaptive', 'web')
            custom_palette: Пользовательская палитра цветов в формате RGB

        Raises:
            InvalidGridSizeError: Если размер сетки не соответствует допустимым значениям
            InvalidParameterError: Если параметры вне допустимого диапазона
        """
        if grid_size not in VALID_GRID_SIZES:
            raise InvalidGridSizeError(f"grid_size должен быть одним из: {VALID_GRID_SIZES}")
        
        if not MIN_NUM_COLORS <= num_colors <= MAX_NUM_COLORS:
            raise InvalidParameterError(f"num_colors должен быть в диапазоне от {MIN_NUM_COLORS} до {MAX_NUM_COLORS}")
        
        if not MIN_SCALE_FACTOR <= scale_factor <= MAX_SCALE_FACTOR:
            raise InvalidParameterError(f"scale_factor должен быть в диапазоне от {MIN_SCALE_FACTOR} до {MAX_SCALE_FACTOR}")
        
        self.grid_size = grid_size
        self.grid_color = grid_color
        self.num_colors = num_colors
        self.scale_factor = scale_factor
        self.background_color = background_color or DEFAULT_BACKGROUND_COLOR
        self.pixelization_algorithm = DEFAULT_PIXELIZATION_ALGORITHM
        self.palette_algorithm = palette_algorithm
        self.custom_palette = custom_palette

    def pixelize(
        self,
        image_path: Union[str, Path],
        output_path: Union[str, Path],
        preset_palette: Optional[str] = None,
    ) -> Dict[int, str]:
        """
        Преобразует изображение в пиксельное с указанными параметрами.

        Args:
            image_path: Путь к входному файлу изображения
            output_path: Путь для сохранения выходного файла
            preset_palette: Название предустановленной палитры ('retro', 'pastel', 'monochrome')

        Returns:
            Словарь с палитрой цветов

        Raises:
            InvalidImageFormatError: Если путь к файлу некорректный
            ImageProcessingError: Если произошла ошибка при обработке изображения
            FileOperationError: Если произошла ошибка при сохранении
        """
        image_path = validate_image_path(image_path)
        output_path = Path(output_path)
        
        # Проверяем формат выходного файла
        if output_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise InvalidImageFormatError(f"Неподдерживаемый формат файла: {output_path.suffix}")

        try:
            # Загрузка и предобработка изображения
            img = Image.open(image_path).convert("RGB")
            size = min(img.width, img.height)
            img = img.crop((0, 0, size, size))
            
            # Пикселизация
            img = img.resize((self.grid_size, self.grid_size), self.pixelization_algorithm)
            
            # Применение палитры
            if preset_palette:
                palette = get_preset_palette(preset_palette)
                img = img.quantize(colors=len(palette), method=Image.Quantize.MEDIANCUT).convert("RGB")
            elif self.custom_palette:
                img = img.quantize(colors=len(self.custom_palette), method=Image.Quantize.MEDIANCUT).convert("RGB")
            else:
                img = img.quantize(colors=self.num_colors, method=PALETTE_ALGORITHMS[self.palette_algorithm]).convert("RGB")

            # Создание увеличенной версии с сеткой
            pixelated_img = img.resize(
                (self.grid_size * self.scale_factor, self.grid_size * self.scale_factor),
                self.pixelization_algorithm
            )

            # Создание нового изображения с фоном
            if self.background_color:
                background = Image.new("RGB", pixelated_img.size, self.background_color)
                background.paste(pixelated_img, (0, 0))
                pixelated_img = background

            # Отрисовка сетки
            draw = ImageDraw.Draw(pixelated_img)
            for i in range(0, pixelated_img.size[0], self.scale_factor):
                draw.line((i, 0, i, pixelated_img.size[1]), fill=self.grid_color)
            for j in range(0, pixelated_img.size[1], self.scale_factor):
                draw.line((0, j, pixelated_img.size[0], j), fill=self.grid_color)

            # Сохранение результата
            save_image(pixelated_img, output_path)
            
            return get_palette_from_image(img)

        except Exception as e:
            raise ImageProcessingError(f"Ошибка при обработке изображения: {str(e)}")
