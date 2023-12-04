import time
import unittest

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class SeleniumUtilTestCase(unittest.TestCase):

    def test_(self):
        """"""
        driver = SeleniumUtil.get_driver()
        driver.get("https://www.baidu.com/")
        # element = SeleniumUtil.find_element(driver, '//input[@id="su"]')
        # print(element)
        # element = SeleniumUtil.find_element(element, './..')
        # print(element)
        value = SeleniumUtil.get_attribute(driver, '//input[@id="su"]', "value")
        print(value)
        time.sleep(1)
        SeleniumUtil.close_browser()
