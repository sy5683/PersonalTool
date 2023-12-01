import os
import typing
from pathlib import Path

from PIL import Image


class ProcessPILImage:
    """处理pil图片"""

    @classmethod
    def add_border(cls, image: Image, border_size: int, color: typing.Tuple[int, int, int]) -> Image:
        """
        添加边框
        实际原理是根据长宽计算出新的背景图片，然后将原图片复制到新背景图片中央
        """
        width, height = image.size
        new_image = cls._create_image((width + border_size * 2, height + border_size * 2), color)
        cls._paste_image_center(new_image, image)
        return new_image

    @classmethod
    def convert_to_jpg(cls, image_path: str, save_path: typing.Union[Path, str]) -> str:
        """转换为jpg图片"""
        image = Image.open(image_path)
        if image.mode == "RGB":
            return image_path
        image.load()
        if image.mode == "RGBA":
            new_image = cls._create_image(image.size)
            new_image.paste(image, mask=image.split()[3])
        else:
            raise Exception(f"未知的图片模式: {image.mode}")
        save_path = f"{os.path.splitext(image_path)[0]}.jpg" if save_path is None else str(save_path)
        image.save(save_path)
        return save_path

    @classmethod
    def to_a4_size(cls, image_path: str, save_path: typing.Union[Path, str]) -> str:
        """将图片转换为A4比例"""
        image = Image.open(image_path)
        printer_width, printer_height = (210, 297)  # A4宽高比
        width, height = new_width, new_height = image.size
        if width > height:
            new_height = width * printer_width // printer_height
        else:
            new_width = height * printer_width // printer_height
        new_image = cls._create_image((new_width, new_height))
        cls._paste_image_center(new_image, image)
        save_path = image_path if save_path is None else str(save_path)
        new_image.save(save_path)
        return save_path

    @staticmethod
    def _create_image(size: typing.Tuple[int, int], color: typing.Tuple[int, int, int] = (255, 255, 255)) -> Image:
        """生成图片对象"""
        return Image.new('RGB', size, color)

    @staticmethod
    def _paste_image_center(new_image: Image, image: Image, **kwargs):
        """将图片复制倒中间"""
        width, height = image.size
        new_width, new_height = new_image.size
        new_image.paste(image, ((new_width - width) // 2, (new_height - height) // 2), **kwargs)
