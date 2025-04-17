from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_utils.control_browser.launch_browser.launch_chrome.launch_chrome import \
    LaunchChrome
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig


class LaunchChromeTestCase(TestBase):

    def setUp(self):
        self.selenium_config = SeleniumConfig()

    def test_get_chrome_path(self):
        chrome_path = LaunchChrome._get_chrome_path(self.selenium_config)
        print(chrome_path)

    def test_get_driver_path(self):
        driver_path = LaunchChrome._get_driver_path(self.selenium_config)
        print(driver_path)
