import unittest

from common_util.code_util.selenium_util.selenium_utils.control_browser.launch_chrome import LaunchChrome


class LaunchChromeTestCase(unittest.TestCase):

    def test_get_chrome_path(self):
        chrome_path = LaunchChrome._get_chrome_path()
        self.assertNotEqual(chrome_path, None)
        print(chrome_path)

    def test_get_chrome_user_data_path(self):
        user_data_path = LaunchChrome._get_chrome_user_data_path()
        self.assertNotEqual(user_data_path, None)
        print(user_data_path)
