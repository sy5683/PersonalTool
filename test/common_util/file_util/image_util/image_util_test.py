import unittest
from pathlib import Path

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.image_util.image_util import ImageUtil


class ImageUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.image_path = Path(__file__).parent.joinpath("测试.png")

    def test_convert_to_jpg_by_opencv(self):
        jpg_path = ImageUtil.convert_to_jpg_by_opencv(self.image_path)
        print(jpg_path)

    def test_convert_to_jpg_by_pil(self):
        jpg_path = ImageUtil.convert_to_jpg_by_pil(self.image_path)
        print(jpg_path)

    def test_remove_border(self):
        ImageUtil.remove_border(self.image_path)

    def test_screenshot(self):
        image_path = ImageUtil.screenshot()
        self.assertNotEqual(image_path, None)
        Win32Util.open_file(image_path)

    def test_to_a4_size(self):
        ImageUtil.to_a4_size(self.image_path)
