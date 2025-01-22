import typing

from playwright.sync_api import *

from ..control_browser.control_browser import ControlBrowser
from ..entity.playwright_config import PlaywrightConfig
from ..enum.operate_type import OperateType


class ControlElement:

    @classmethod
    def click(cls, playwright_config: PlaywrightConfig):
        """模拟点击"""
        if playwright_config.operate_type == OperateType.js:
            cls.find(playwright_config).evaluate("element => element.click()")
        else:
            wait_seconds = playwright_config.wait_seconds
            playwright_config.wait_seconds = 1
            for index in range(wait_seconds):
                if index:
                    playwright_config.logger = None
                try:
                    cls.find(playwright_config).click()
                except TimeoutError:
                    continue
                break
            else:
                raise Exception("点击失败")

    @classmethod
    def find(cls, playwright_config: PlaywrightConfig) -> Locator:
        """查找元素"""
        # 当存在xpath的情况下，优先定位xpath对应的元素
        if playwright_config.xpath:
            playwright_config.info(f"查找元素: {playwright_config.xpath}")
            # 当有多个元素时，直接调用点击方法时会报错，因此最好先使用finds方法获取全部元素，再返回第一个
            playwright_config.logger = None
            locators = cls.finds(playwright_config)
            return locators[0]
        # 当xpath不存在的情况下，返回参数中的locator，如果也为空，则需要报错
        if playwright_config.locator is None:
            raise AttributeError("参数中的xpath与locator均为空，无法定位元素")
        return playwright_config.locator

    @classmethod
    def finds(cls, playwright_config: PlaywrightConfig) -> typing.List[Locator]:
        """查找元素列表"""
        playwright_config.info(f"查找元素列表: {playwright_config.xpath}")
        return cls.__finds(playwright_config)

    @classmethod
    def get_attribute(cls, playwright_config: PlaywrightConfig, attribute_type: str) -> str:
        """获取元素内容"""
        return cls.find(playwright_config).get_attribute(attribute_type)

    @classmethod
    def input(cls, playwright_config: PlaywrightConfig, value: str):
        """输入"""


    @classmethod
    def __finds(cls, playwright_config: PlaywrightConfig) -> typing.List[Locator]:
        """查找元素列表"""
        if not playwright_config.xpath:
            raise ValueError("查找元素方法必须传入xpath")
        page = cls.__get_page(playwright_config) if playwright_config.locator is None else playwright_config.locator
        # 注: playwright并没有显性等待和隐性等待的区别，其拥有的自动等待功能类似于隐性等待，默认为30s
        return page.locator(playwright_config.xpath).all()

    @staticmethod
    def __get_page(playwright_config: PlaywrightConfig) -> Page:
        """根据参数获取page"""
        if playwright_config.page is None:
            browser, playwright_config.context, playwright_config.page = ControlBrowser.get_driver(playwright_config)
        return playwright_config.page
