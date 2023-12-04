import logging
import time

from selenium import webdriver

from .control_element import ControlElement


class ControlIframe:
    """控制iframe"""

    @staticmethod
    def switch_iframe(driver: webdriver, xpath: str, wait_seconds: int):
        """切换iframe"""
        # 1) 没有传入xpath时将iframe切换至默认层
        if not xpath:
            logging.info("切换至默认iframe")
            driver.switch_to.default_content()
        # 2) 切换至父级iframe。因为元素的父级也是这个xpath，因此这里使用一样的语法处理
        elif xpath == "..":
            driver.switch_to.parent_frame()
        # 3) 切换至指定iframe
        else:
            iframe_element = ControlElement.find_element(driver, xpath, wait_seconds)
            driver.switch_to.frame(iframe_element)
        # iframe切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(1)
