import typing
from pathlib import Path

import cv2

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil


class ImageFeature:

    @classmethod
    def matting_characters(cls, file_paths: typing.List[str], color: int = 255):
        """扣取文字"""
        image_paths = cls.__to_image_paths(file_paths)
        for image_path in image_paths:
            # 读取图片
            image = ImageUtil.read_opencv_image(image_path)
            # 去除边框
            image = ImageUtil.remove_border(image, color)
            # 生成蒙版
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rect, mask_image = cv2.threshold(gray_image, color, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            # 使用蒙版将图片将图片背景透明化
            transparent_image = ImageUtil.image_to_transparent(image, mask_image)
            # 保存图片
            save_path = FileUtil.get_temp_path(Path(image_path).name)
            ImageUtil.save_opencv_image(transparent_image, save_path)
        Win32Util.open_file(FileUtil.get_temp_path())

    @staticmethod
    def __to_image_paths(file_paths: typing.List[str]):
        image_paths = []
        for file_path in file_paths:
            if FileUtil.get_original_type(file_path) == "pdf":
                image_paths += PdfUtil.pdf_to_images(file_path)
            else:
                image_paths += [file_path]
        return image_paths
