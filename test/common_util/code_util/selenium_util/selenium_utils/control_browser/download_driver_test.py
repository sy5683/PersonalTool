from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_utils.control_browser.launch_browser.download_driver import \
    DownloadDriver


class DownloadDriverTestCase(TestBase):

    def test_get_chrome_driver_path(self):
        chrome_driver_path = DownloadDriver.get_chrome_driver_path()
        self.assertNotEqual(chrome_driver_path, None)
        print(chrome_driver_path)

    def test_get_edge_driver_path(self):
        edge_driver_path = DownloadDriver.get_edge_driver_path()
        self.assertNotEqual(edge_driver_path, None)
        print(edge_driver_path)
