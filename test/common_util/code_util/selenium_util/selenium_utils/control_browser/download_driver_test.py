import unittest

from common_util.code_util.selenium_util.selenium_utils.control_browser.download_driver import DownloadDriver


class DownloadDriverTestCase(unittest.TestCase):

    def test_get_chrome_driver_path(self):
        driver_path = DownloadDriver.get_chrome_driver_path()
        self.assertNotEqual(driver_path, None)
        print(driver_path)

    def test_get_edge_driver_path(self):
        driver_path = DownloadDriver.get_edge_driver_path()
        self.assertNotEqual(driver_path, None)
        print(driver_path)

    def test_get_ie_driver_path(self):
        driver_path = DownloadDriver.get_ie_driver_path()
        self.assertNotEqual(driver_path, None)
        print(driver_path)
