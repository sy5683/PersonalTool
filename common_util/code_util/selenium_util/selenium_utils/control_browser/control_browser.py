import typing

from selenium.webdriver.chrome.webdriver import WebDriver

from .browser_type import BrowserType
from .launch_browser.base.launch_base import LaunchBase
from .launch_browser.launch_chrome import LaunchChrome
from .launch_browser.launch_edge import LaunchEdge
from .launch_browser.launch_ie import LaunchIe
from ..selenium_config import SeleniumConfig


class ControlBrowser:

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        return cls._get_launch_class().get_driver(**kwargs)

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭浏览器"""
        cls._get_launch_class().close_browser(**kwargs)

    @staticmethod
    def _get_launch_class() -> typing.Type[LaunchBase]:
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome
        elif SeleniumConfig.browser_type == BrowserType.edge:
            return LaunchEdge
        elif SeleniumConfig.browser_type == BrowserType.ie:
            return LaunchIe
        else:
            raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")
