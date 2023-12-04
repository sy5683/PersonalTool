import logging
import unittest

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class SeleniumUtilTestCase(unittest.TestCase):

    def test_get_driver(self):
        driver = SeleniumUtil.get_driver()
        self.assertNotEqual(driver, None)
        print(driver)
