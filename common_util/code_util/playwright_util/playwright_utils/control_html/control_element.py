import typing

from playwright import sync_api

from ..entity.playwright_config import PlaywrightConfig
from ..enum.operate_type import OperateType


class ControlElement:

    @classmethod
    def click(cls, playwright_config: PlaywrightConfig):
        """模拟点击"""
        if playwright_config.operate_type == OperateType.js:
            pass
        else:
            wait_seconds = playwright_config.wait_seconds
            playwright_config.wait_seconds = 1
            for index in range(wait_seconds):
                if index:
                    playwright_config.logger = None
                try:
                    pass  # TODO
                except IndexError:  # TODO
                    continue
                break
            else:
                raise Exception("点击失败")

    @classmethod
    def find(cls, playwright_config: PlaywrightConfig) -> sync_api.Locator:
        """查找元素"""
        # 当存在xpath的情况下，优先定位xpath对应的元素
        if playwright_config.xpath:
            playwright_config.info(f"查找元素: {playwright_config.xpath}")

    @classmethod
    def finds(cls, playwright_config: PlaywrightConfig) -> typing.List[sync_api.Locator]:
        """查找元素列表"""
        playwright_config.info(f"查找元素列表: {playwright_config.xpath}")

    @classmethod
    def _click_by_js(cls, playwright_config: PlaywrightConfig):
        """通过js点击元素"""
        for locator in cls.find(playwright_config).all():
            try:
                locator.evaluate('element => element.click()')
                break
            except Exception:
                pass

    @classmethod
    def _click_by_playwright(cls, playwright_config: PlaywrightConfig):
        """通过playwright自带方式点击元素"""

    @classmethod
    def __find(cls, playwright_config: PlaywrightConfig, 
               find_method) -> typing.Union[sync_api.Locator, typing.List[sync_api.Locator]]:
        """显性等待查找元素"""
        if not playwright_config.xpath:
            raise ValueError("查找元素方法必须传入xpath")
        page = ""
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错，因此这里将间隔时间修改为0.3s）
