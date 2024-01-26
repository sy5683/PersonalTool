import unittest
from pathlib import Path

from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.image_util.image_utils.screenshot import Screenshot


class ScreenshotTestCase(unittest.TestCase):

    def test_screenshot(self):
        images = Screenshot.screenshot()
        self.assertNotEqual(images, None)
        for index, image in enumerate(images):
            image_path = Path(__file__).parent.joinpath(f"{index}.png")
            ImageUtil.save_opencv_image(image, image_path)
