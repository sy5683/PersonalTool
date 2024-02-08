from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.file_util.file_util.file_util import FileUtil
from feature.image_feature.cv2_remove_background import Cv2RemoveBackground
from feature.image_feature.pp_remove_background import PPRemoveBackground


class Operations(Enum):
    matting_character = Cv2RemoveBackground.matting_character
    matting_picture = PPRemoveBackground.matting_picture


class ImageProcessor(ToolBase):

    def __init__(self):
        self.file_paths = FileUtil.get_file_paths()
        assert self.file_paths, "未选择文件"

    def main(self, function, **kwargs):
        function(self.file_paths, **kwargs)


if __name__ == '__main__':
    image_processor = ImageProcessor()
    # image_processor.main(Operations.matting_character, color=125)
    image_processor.main(Operations.matting_picture, background_color=(0, 0, 255))
