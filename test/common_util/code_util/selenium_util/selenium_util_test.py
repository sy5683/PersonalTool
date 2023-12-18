import logging
import time
import unittest
from concurrent import futures

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class SeleniumUtilTestCase(unittest.TestCase):
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None,
                        filemode='a')

    def _launch_driver(self):
        driver = SeleniumUtil.get_driver(use_user_data=False)
        SeleniumUtil.open_url("https://www.baidu.com/", use_user_data=False)  # 多并发时不能使用user_data
        element = SeleniumUtil.find('//input[@id="su"]')
        print(f"1: {element}")
        element = SeleniumUtil.find('./ancestor::form[@id="form"]', element=element)
        print(f"2: {element}")
        time.sleep(1)
        SeleniumUtil.close_browser(driver=driver)

    def test_(self):
        """"""
        pool = futures.ThreadPoolExecutor(3, thread_name_prefix="test")
        tasks = []
        for _ in range(3):
            tasks.append(pool.submit(self._launch_driver))
        for task in futures.as_completed(tasks):
            print(task.result())
