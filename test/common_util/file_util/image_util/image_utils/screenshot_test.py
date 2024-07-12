import cv2

from common_core.base.test_base import TestBase
from common_util.file_util.image_util.image_utils.screenshot import Screenshot


class ScreenshotTestCase(TestBase):

    def test_get_screenshot_images(self):
        screenshot_images = Screenshot.get_screenshot_images()
        self.assertNotEqual(screenshot_images, [])
        for screenshot_image in screenshot_images:
            cv2.imshow("show_name", screenshot_image)
            cv2.waitKey(0)
