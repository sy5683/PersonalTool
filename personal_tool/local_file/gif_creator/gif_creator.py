import logging
import os.path
import tempfile
import tkinter
import uuid
from tkinter import filedialog
from typing import List

import cv2
import imageio
import win32api
from cv2 import warpAffine
from numpy import fabs, sin, cos, radians

from personal_tool.base.tool_base import ToolBase


class GifCreator(ToolBase):
    """gif生成器"""

    def __init__(self, duration: float = 0.1):
        self.duration = duration
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        self.image_paths = filedialog.askopenfilenames()
        self.save_dir_path = tempfile.mkdtemp()

    def main(self, function=None, **kwargs):
        if self.image_paths:
            logging.info("开始生成gif..")
            if function:
                function(self, **kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", self.save_dir_path, "", "", 1)

    def make_rotate_gif(self, angle: int):
        """生成旋转的gif"""
        for image_path in self.image_paths:
            image = cv2.imread(image_path)
            image_gifs = []
            for each in range(360 // angle):
                image_height, image_width = image.shape[:2]
                image_center = (image_width // 2, image_height // 2)
                new_height = int(image_width * fabs(sin(radians(angle))) + image_height * fabs(cos(radians(angle))))
                new_width = int(image_height * fabs(sin(radians(angle))) + image_width * fabs(cos(radians(angle))))
                image_rotate = cv2.getRotationMatrix2D(image_center, angle * each, 1)
                image_rotate[0, 2] += (new_width - image_width) // 2
                image_rotate[1, 2] += (new_height - image_height) // 2
                image_gif = cv2.warpAffine(image, image_rotate, (new_width, new_height))
                image_gifs.append(image_gif)
            self._save_gif(image_gifs)

    def _save_gif(self, gifs: List[warpAffine]):
        """生成gif"""
        gif_path = os.path.join(self.save_dir_path, f"temp_gif_{str(uuid.uuid4())}.gif")
        return imageio.mimsave(gif_path, gifs, 'GIF', duration=self.duration)


if __name__ == '__main__':
    gif_creator = GifCreator()
    gif_creator.main(GifCreator.make_rotate_gif, angle=2)
