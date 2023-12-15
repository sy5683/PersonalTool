import logging

from selenium.webdriver.chrome.webdriver import WebDriver

from .browser_type import BrowserType
from .launch_chrome import LaunchChrome
from .launch_edge import LaunchEdge
from .launch_ie import LaunchIe
from ..selenium_config import SeleniumConfig


class ControlBrowser:

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        debug_port = cls.__format_debug_port(**kwargs)
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome.get_driver(debug_port)
        else:
            if debug_port:
                logging.warning(f"只有谷歌浏览器才可以使用debug接管浏览器: {SeleniumConfig.browser_type.value}")
            if SeleniumConfig.browser_type == BrowserType.edge:
                return LaunchEdge.get_driver()
            elif SeleniumConfig.browser_type == BrowserType.ie:
                return LaunchIe.get_driver()
            else:
                raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭浏览器"""
        debug_port = cls.__format_debug_port(**kwargs)
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome.close_browser(debug_port)
        elif SeleniumConfig.browser_type == BrowserType.edge:
            return LaunchEdge.close_browser()
        elif SeleniumConfig.browser_type == BrowserType.ie:
            return LaunchIe.get_driver()
        else:
            raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")

    @staticmethod
    def __format_debug_port(**kwargs) -> int:
        return kwargs.get("debug_port", 0)
