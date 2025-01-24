import re
import time
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
    def exist(cls, playwright_config: PlaywrightConfig) -> bool:
        """查找元素是否存在"""
        try:
            locator = cls.find(playwright_config)
            assert [locator.text_content()] is not None  # 这一行是为了检测入参为WebElement的元素
        except (AssertionError,):
            return False
        return True

    @classmethod
    def find(cls, playwright_config: PlaywrightConfig) -> Locator:
        """查找元素"""
        # 当存在xpath的情况下，优先定位xpath对应的元素
        if playwright_config.xpath:
            playwright_config.info(f"查找元素: {playwright_config.xpath}")
            # 当有多个元素时，直接调用点击方法时会报错，因此最好先使用finds方法获取全部元素，再返回第一个
            return cls.finds(playwright_config)[0]
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
        locator = cls.find(playwright_config)
        if attribute_type == "innerText":
            return locator.inner_text()
        else:
            return locator.get_attribute(attribute_type)

    @classmethod
    def input(cls, playwright_config: PlaywrightConfig, value: str):
        """输入"""
        # playwright框架定位有问题，暂不支持action操作
        locator = cls.find(playwright_config)
        playwright_config.info("输入元素: %s" % ("*" * len(value) if cls.__check_is_password(locator) else value))
        for _ in range(3):
            # 先清空元素内容
            cls._clear_locator(locator)
            # 模拟全选
            locator.press("Control+A")
            time.sleep(0.2)
            # 输入元素
            locator.fill(value)
            # 密码无需判断输入结果
            if cls.__check_is_password(locator):
                break
            # 某些特殊情况无需判断输入结果: 日期格式化、金额会计格式化等
            if not playwright_config.check_input:
                break
            # 判断输入结果是否正确
            locator_value = locator.input_value()
            if locator_value == value:
                break
            playwright_config.info(f"重新输入，元素的值为: {locator_value}")
        else:
            raise RuntimeError(f"元素输入失败: {value}")

    @classmethod
    def wait_disappear(cls, playwright_config: PlaywrightConfig) -> bool:
        """
        等待元素消失
        需要注意的是，检测元素消失的前提是这个元素已经出现
        使用时需要注意，不要在做完上一个操作之后立马调用这个方法，不然可能会出现【要检测消失的元素还未出现，这个方法就已经判断该元素已消失】
        在使用时需要根据具体情况在前面加一定时间的强制等待
        """
        wait_seconds = playwright_config.wait_seconds
        playwright_config.wait_seconds = 1
        for _ in range(wait_seconds):
            time.sleep(1)  # 等待元素加载
            if not cls.exist(playwright_config):
                return True
        return False

    @staticmethod
    def _clear_locator(locator: Locator):
        """清空元素"""
        # 先点击定位
        locator.click()
        pass  # 元素可能无法点击  TODO
        time.sleep(0.2)
        # 使用playwright自带的clear方法
        locator.clear()
        pass  # 元素可能无法清空
        time.sleep(0.2)
        # 有时候有输入框 locator.clear() 方法无效，因此再使用手动清空方式
        for _ in range(len(locator.get_attribute("value"))):
            locator.press("ArrowRight")
            locator.press("Backspace")
            time.sleep(0.1)

    @staticmethod
    def __check_is_password(locator: Locator) -> bool:
        """判断元素是否为密码类"""
        return locator.get_attribute("type") == "password"

    @classmethod
    def __finds(cls, playwright_config: PlaywrightConfig) -> typing.List[Locator]:
        """查找元素列表"""
        if not playwright_config.xpath:
            raise ValueError("查找元素方法必须传入xpath")
        page = cls.__get_page(playwright_config) if playwright_config.locator is None else playwright_config.locator
        time.sleep(playwright_config.delay_seconds)
        # playwright中没有类似selenium的显性等待与隐性等待，因此这里模拟实现一个
        for _ in range(playwright_config.wait_seconds):
            if re.search("//iframe\[", playwright_config.xpath):
                locators = [page.frame_locator(playwright_config.xpath)]
            else:
                locators = page.locator(playwright_config.xpath).all()
            # locator.all()方法在未查到元素时不会报错，而是返回一个空列表出去
            if locators:
                return locators
            time.sleep(1)
        raise AttributeError(f"未找到指定元素: {playwright_config.xpath}")

    @staticmethod
    def __get_page(playwright_config: PlaywrightConfig) -> Page:
        """根据参数获取page"""
        if playwright_config.page is None:
            browser, playwright_config.context, playwright_config.page = ControlBrowser.get_driver(playwright_config)
        return playwright_config.page
