import win32api

from gif_maker.feature.image_feature import ImageFeature
from gif_maker.make_rotate_gif import MakeRotateGif


class GifMaker:
    """gif生成器"""

    def __init__(self, duration: float = 0.1):
        self.duration = duration  # 每张图片播放时间

    def main(self, function=None, **kwargs):
        if function and ImageFeature.get_image_paths():
            kwargs['duration'] = self.duration
            function(**kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", ImageFeature.get_save_path(), "", "", 1)


if __name__ == '__main__':
    gif_maker = GifMaker()
    gif_maker.main(MakeRotateGif.make_rotate_gif, angle=2)
