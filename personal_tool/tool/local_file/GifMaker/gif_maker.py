import uuid

import cv2
import imageio
import win32api
from PIL import Image

from personal_tool.base.tool_base import ToolBase
from personal_tool.tool.local_file.GifMaker.gif_maker.feature.image_feature import ImageFeature


class GifMaker(ToolBase):

    def __init__(self, duration: float = 0.1):
        super().__init__("gif生成器")
        self.duration = duration  # 每张图片播放时间

    def main(self, function=None, **kwargs):
        if function and ImageFeature.get_image_paths():
            function(self, **kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", ImageFeature.get_save_path(), "", "", 1)

    def make_rotate_gif(self, angle: int):
        """生成旋转的gif"""
        for image_path in ImageFeature.get_image_paths():
            rotate_images = []
            # """PIL 实现旋转时会出现严重的锯齿"""
            # image = Image.open(image_path)
            # for times in range(360 // angle):
            #     rotate_images.append(image.rotate(angle * times))
            # gif_path = ImageFeature.get_save_path(f"temp_gif_{str(uuid.uuid4())}.gif")
            # image.save(gif_path, save_all=True, append_images=rotate_images[1:], duration=self.duration)
            """cv2 实现生成的gif背景不透明"""
            image = cv2.imread(image_path)
            for times in range(360 // angle):
                rotate_image = ImageFeature.image_rotate(image, angle, times)
                rotate_images.append(rotate_image)
            gif_path = ImageFeature.get_save_path(f"temp_gif_{str(uuid.uuid4())}.gif")
            imageio.mimsave(gif_path, rotate_images, 'GIF', duration=self.duration)


if __name__ == '__main__':
    gif_maker = GifMaker()
    gif_maker.main(GifMaker.make_rotate_gif, angle=2)
