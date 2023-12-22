import logging
import time
import typing

from selenium.webdriver.remote.webelement import WebElement

from .control_element import ControlElement
from ..control_browser.control_browser import ControlBrowser


class ControlIframe:
    """控制iframe"""

    @staticmethod
    def switch_iframe(element_or_xpath: typing.Union[WebElement, str], **kwargs):
        """切换iframe"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        if isinstance(element_or_xpath, str):
            if not element_or_xpath:
                logging.info("切换至默认iframe")
                driver.switch_to.default_content()
            elif element_or_xpath == "..":  # 因为元素的父级也是这个xpath，因此这里使用一样的语法处理
                logging.info("切换至父级iframe")
                driver.switch_to.parent_frame()
            else:
                element_or_xpath = ControlElement.find(xpath=element_or_xpath, **kwargs)
        if isinstance(element_or_xpath, WebElement):
            logging.info(f"切换至指定iframe: {element_or_xpath}")
            driver.switch_to.frame(element_or_xpath)
        # iframe切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(0.1)
