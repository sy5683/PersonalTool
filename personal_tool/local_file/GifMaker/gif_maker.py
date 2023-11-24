from enum import Enum

from gif_maker.feature.image_feature import ImageFeature
from gif_maker.make_rotate_gif import MakeRotateGif
from gif_maker.util.win32_util import Win32Util


class Operations(Enum):
    make_rotate_gif = MakeRotateGif.make_rotate_gif


class GifMaker:
    """gif生成器"""

    def __init__(self, duration: float = 0.1):
        self.image_paths = ImageFeature.get_image_paths()
        self.duration = duration  # 每张图片播放时间

    def main(self, function, **kwargs):
        if self.image_paths:
            kwargs['duration'] = self.duration
            function(**kwargs)
            Win32Util.open_file(ImageFeature.get_save_path())


if __name__ == '__main__':
    gif_maker = GifMaker()
    gif_maker.main(Operations.make_rotate_gif, angle=2)
