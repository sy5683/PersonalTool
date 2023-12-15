import logging
import time
import unittest

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class SeleniumUtilTestCase(unittest.TestCase):
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None,
                        filemode='a')

    def test_(self):
        """"""
        # SeleniumUtil.launch_chrome_debug()
        # driver_1 = SeleniumUtil.get_driver()
        # SeleniumUtil.launch_chrome_debug(8222)
        # driver_2 = SeleniumUtil.get_driver(8222)
        # driver_1.get("https://www.baidu.com/")
        # driver_2.get("https://fanyi.baidu.com/")

        SeleniumUtil.open_url("https://www.baidu.com/")
        element = SeleniumUtil.find('//input[@id="su"]')
        print(element)
        element = SeleniumUtil.find('./ancestor::form[@id="kw"]', element=element)
        print(element)
        time.sleep(1)
        SeleniumUtil.close_browser()
