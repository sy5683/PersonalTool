import uuid

import cv2
import imageio
import numpy as np
from PIL import Image

from .feature.image_feature import ImageFeature


class MakeRotateGif:

    @staticmethod
    def make_rotate_gif(angle: int, duration: float, func_way='cv2'):
        """生成旋转的gif"""
        for image_path in ImageFeature.get_image_paths():
            rotate_images = []
            gif_path = ImageFeature.get_save_path(f"temp_gif_{str(uuid.uuid4())}.gif")

            if func_way == "cv2":
                # TODO cv2实现生成的gif背景不透明，需要寻找优化方案
                image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
                for times in range(360 // angle):
                    rotate_image = ImageFeature.image_rotate(image, angle, times)
                    rotate_images.append(rotate_image)
                imageio.mimsave(gif_path, rotate_images, 'GIF', duration=duration)
            else:
                # TODO PIL实现旋转时会出现严重的锯齿，仅记录，之后废弃
                image = Image.open(image_path)
                for times in range(360 // angle):
                    rotate_images.append(image.rotate(angle * times))
                image.save(gif_path, save_all=True, append_images=rotate_images[1:], duration=duration)
