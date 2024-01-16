import unittest

from common_util.code_util.selenium_util.selenium_utils.control_browser.download_driver import DownloadDriver


class DownloadDriverTestCase(unittest.TestCase):

    def test_get_chrome_driver_path(self):
        chrome_driver_path = DownloadDriver.get_chrome_driver_path()
        self.assertNotEqual(chrome_driver_path, None)
        print(chrome_driver_path)
