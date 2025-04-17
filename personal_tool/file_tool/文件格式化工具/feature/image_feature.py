import os

from common_util.file_util.image_util.image_util import ImageUtil


class ImageFeature:

    @staticmethod
    def webp_to_jpg(image_path: pathlib.Path) -> str:
        """webp图片转换为jpg图片"""
        new_image_path = ImageUtil.convert_to_jpg_by_pil(image_path)
        os.remove(image_path)
        return new_image_path
