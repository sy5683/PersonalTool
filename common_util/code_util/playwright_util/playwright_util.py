import typing

from playwright.sync_api import *

from .playwright_utils.control_browser.control_browser import ControlBrowser
from .playwright_utils.control_html.control_driver import ControlDriver
from .playwright_utils.control_html.control_element import ControlElement
from .playwright_utils.entity.playwright_config import PlaywrightConfig


class PlaywrightUtil:

    @staticmethod
    def click(playwright_config: PlaywrightConfig):
        """模拟点击"""
        ControlElement.click(playwright_config)

    @staticmethod
    def find(playwright_config: PlaywrightConfig) -> Locator:
        """查找元素"""
        return ControlElement.find(playwright_config)

    @staticmethod
    def finds(playwright_config: PlaywrightConfig) -> typing.List[Locator]:
        """查找元素列表"""
        return ControlElement.finds(playwright_config)

    @staticmethod
    def get_attribute(playwright_config: PlaywrightConfig, attribute_type: str) -> str:
        """获取元素内容，常用的值有: id, class, value, innerText"""
        return ControlElement.get_attribute(playwright_config, attribute_type)

    @staticmethod
    def get_driver(playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """获取句柄browser, context, page"""
        return ControlBrowser.get_driver(playwright_config)

    @staticmethod
    def input(playwright_config: PlaywrightConfig, value: typing.Union[float, str]):
        """输入"""
        ControlElement.input(playwright_config, str(value))

    @staticmethod
    def open_url(playwright_config: PlaywrightConfig, url: str):
        """打开url"""
        ControlDriver.open_url(playwright_config, url)

    @staticmethod
    def refresh(playwright_config: PlaywrightConfig):
        """刷新"""
        ControlDriver.refresh(playwright_config)
