import time

from selenium import common

from .control_element import ControlElement
from ..control_browser.control_browser import ControlBrowser
from ..entity.selenium_config import SeleniumConfig


class ControlIframe:

    @staticmethod
    def switch_iframe(selenium_config: SeleniumConfig):
        """切换iframe"""
        driver = ControlBrowser.get_driver(selenium_config)
        # 根据xpath切换至父级iframe
        if selenium_config.xpath == "..":  # 因为元素的父级也是这个xpath，因此这里使用一样的语法处理
            selenium_config.info("切换至父级iframe")
            driver.switch_to.parent_frame()
        # 根据xpath或element切换至指定iframe
        else:
            try:
                selenium_config.info(f"切换至指定iframe: {selenium_config.xpath}")
                driver.switch_to.frame(ControlElement.find(selenium_config))
            except (AttributeError, common.exceptions.NoSuchWindowException):
                # 没有需要定位的iframe且xpath为空时，切换至默认iframe
                if not selenium_config.xpath:
                    selenium_config.info("切换至默认iframe")
                    driver.switch_to.default_content()
        # iframe切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(0.1)
