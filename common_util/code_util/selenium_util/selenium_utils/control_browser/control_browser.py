import typing

from selenium.webdriver.chrome.webdriver import WebDriver

from .launch_browser.base.launch_base import LaunchBase
from .launch_browser.launch_chrome.launch_chrome import LaunchChrome
from .launch_browser.launch_edge.launch_edge import LaunchEdge
from .launch_browser.launch_ie.launch_ie import LaunchIe
from ..entity.selenium_config import SeleniumConfig
from ..enum.browser_type import BrowserType


class ControlBrowser:

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭浏览器"""
        cls._get_launch_class(selenium_config.browser_type).close_browser(selenium_config)

    @classmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        return cls._get_launch_class(selenium_config.browser_type).get_driver(selenium_config)

    @staticmethod
    def _get_launch_class(browser_type: BrowserType) -> typing.Type[LaunchBase]:
        if browser_type == BrowserType.chrome:
            return LaunchChrome
        elif browser_type == BrowserType.edge:
            return LaunchEdge
        elif browser_type == BrowserType.ie:
            return LaunchIe
        else:
            raise TypeError(f"暂不支持的浏览器类型: {browser_type.name}")
