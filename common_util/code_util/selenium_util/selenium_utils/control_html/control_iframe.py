import logging
import time
import typing

from selenium.webdriver.remote.webelement import WebElement

from .control_element import ControlElement
from ..control_browser.control_browser import ControlBrowser


class ControlIframe:
    """控制iframe"""

    @staticmethod
    def switch_iframe(key: typing.Union[str, WebElement], **kwargs):
        """切换iframe"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        if isinstance(key, str):
            if not key:
                logging.info("切换至默认iframe")
                driver.switch_to.default_content()
            elif key == "..":  # 因为元素的父级也是这个xpath，因此这里使用一样的语法处理
                logging.info("切换至父级iframe")
                driver.switch_to.parent_frame()
            else:
                key = ControlElement.find(xpath=key, **kwargs)
        if isinstance(key, WebElement):
            logging.info(f"切换至指定iframe: {key}")
            driver.switch_to.frame(key)
        # iframe切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(0.1)
