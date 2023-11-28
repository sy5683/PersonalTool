from enum import Enum

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.file_util.file_util import FileUtil
from gif_maker.make_rotate_gif import MakeRotateGif


class Operations(Enum):
    make_rotate_gif = MakeRotateGif.make_rotate_gif


class GifMaker:
    """gif生成器"""

    def __init__(self):
        self.image_paths = FileUtil.get_file_paths()

    def main(self, function, **kwargs):
        if self.image_paths:
            function(self.image_paths, **kwargs)
            Win32Util.open_file(FileUtil.get_temp_path())


if __name__ == '__main__':
    gif_maker = GifMaker()
    gif_maker.main(Operations.make_rotate_gif, angle=2)
