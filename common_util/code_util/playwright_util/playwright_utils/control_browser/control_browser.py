import typing

from playwright.sync_api import *

from .launch_browser.base.launch_base import LaunchBase
from .launch_browser.launch_chrome import LaunchChrome
from ..entity.playwright_config import PlaywrightConfig
from ..enum.browser_type import BrowserType


class ControlBrowser:

    @classmethod
    def close_browser(cls, playwright_config: PlaywrightConfig):
        """关闭浏览器"""
        cls._get_launch_class(playwright_config.browser_type).close_browser(playwright_config)

    @classmethod
    def get_driver(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """获取driver"""
        return cls._get_launch_class(playwright_config.browser_type).get_driver(playwright_config)

    @staticmethod
    def _get_launch_class(browser_type: BrowserType) -> typing.Type[LaunchBase]:
        if browser_type == BrowserType.chrome:
            return LaunchChrome
        else:
            raise TypeError(f"暂不支持的浏览器类型: {browser_type.name}")
