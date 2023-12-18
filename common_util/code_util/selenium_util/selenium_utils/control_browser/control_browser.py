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
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome.get_driver(**kwargs)
        else:
            if SeleniumConfig.browser_type == BrowserType.edge:
                return LaunchEdge.get_driver()
            elif SeleniumConfig.browser_type == BrowserType.ie:
                return LaunchIe.get_driver()
            else:
                raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭浏览器"""
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome.close_browser(**kwargs)
        elif SeleniumConfig.browser_type == BrowserType.edge:
            return LaunchEdge.close_browser()
        elif SeleniumConfig.browser_type == BrowserType.ie:
            return LaunchIe.get_driver()
        else:
            raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")
