import os
import typing

from PIL import Image


class ProcessPILImage:

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
    def convert_to_jpg(cls, image_path: str, save_path: typing.Union[pathlib.Path, str]) -> str:
        """转换为jpg图片"""
        with Image.open(image_path) as image:
            image.load()
            if image.mode == "RGB":
                new_image = image
            elif image.mode == "RGBA":
                new_image = cls._create_image(image.size)
                new_image.paste(image, mask=image.split()[3])
            else:
                raise TypeError(f"未知的图片模式: {image.mode}")
            save_path = f"{os.path.splitext(image_path)[0]}.jpg" if save_path is None else str(save_path)
            new_image.save(save_path)
        return save_path

    @classmethod
    def re_scale(cls, image_path: str, new_size: typing.Tuple[int, int], save_path: typing.Union[pathlib.Path, str],
                 resize: bool) -> str:
        """转换图片比例"""
        new_width, new_height = new_size
        with Image.open(image_path) as image:
            width, height = _new_width, _new_height = image.size
            if width / height > new_width / new_height:
                _new_height = width * new_height // new_width
            else:
                _new_width = height * new_width // new_height
            new_image = cls._create_image((_new_width, _new_height))
            cls._paste_image_center(new_image, image)
        if resize:
            new_image = new_image.resize(new_size)
        _image_path, suffix = os.path.splitext(image_path)
        save_path = f"{_image_path}{new_size}{suffix}" if save_path is None else str(save_path)
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
