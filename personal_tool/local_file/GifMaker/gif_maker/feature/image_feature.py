import os.path
import tempfile
import tkinter
import typing
from tkinter import filedialog

import cv2
from numpy import cos, fabs, radians, sin
from numpy import ndarray


class ImageFeature:
    _image_paths = None
    _save_dir_path = None

    @classmethod
    def get_image_paths(cls) -> typing.List[str]:
        if cls._image_paths is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._image_paths = filedialog.askopenfilenames()
        return cls._image_paths

    @classmethod
    def get_save_path(cls, image_name: str = '') -> str:
        if cls._save_dir_path is None:
            cls._save_dir_path = tempfile.mkdtemp()
        return os.path.join(cls._save_dir_path, image_name)

    @staticmethod
    def image_rotate(image: ndarray, angle: int, times: int) -> ndarray:
        """图片旋转"""
        height, width = image.shape[:2]
        new_height = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
        new_width = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))
        rotate_image = cv2.getRotationMatrix2D((width // 2, height // 2), angle * times, 1)
        rotate_image[0, 2] += (new_width - width) // 2
        rotate_image[1, 2] += (new_height - height) // 2
        return cv2.warpAffine(image, rotate_image, (new_width, new_height))
