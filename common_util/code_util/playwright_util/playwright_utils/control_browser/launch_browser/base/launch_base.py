import abc
import typing

from playwright.sync_api import *

from ....entity.playwright_config import PlaywrightConfig


class LaunchBase(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def close_browser(cls, playwright_config: PlaywrightConfig):
        """关闭浏览器"""

    @classmethod
    @abc.abstractmethod
    def get_driver(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """获取句柄browser, context, page"""

    @staticmethod
    def set_browser_front(page: Page):
        """设置浏览器最前端"""
        # page.set_viewport_size({'width': 1920, 'height': 1080})
        pass  # TODO 方法待实现
