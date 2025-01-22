import logging
import typing

from playwright.sync_api import *

from ..enum.browser_type import BrowserType
from ..enum.operate_type import OperateType


class PlaywrightConfig:

    def __init__(self,
                 browser: Browser = None,
                 browser_type: BrowserType = BrowserType.chrome,
                 check_input: bool = True,
                 context: BrowserContext = None,
                 debug_port: int = None,
                 delay_seconds: int = 0,
                 headless: bool = False,
                 locator: Locator = None,
                 logger: typing.Union[logging.Logger, None] = logging.getLogger(),
                 operate_type: OperateType = OperateType.js,
                 page: Page = None,
                 xpath: str = '',
                 wait_seconds: int = 120,
                 ):
        self.browser = browser  # playwright运行的browser对象
        self.browser_type = browser_type  # 浏览器类型，默认为谷歌浏览器
        self.check_input = check_input  # 检测输入内容是否正确
        self.context = context  # playwright运行的context对象
        self.debug_port = debug_port  # debug端口，用于接管浏览器
        self.delay_seconds = delay_seconds  # 演示时间，默认为0不等待
        self.headless = headless  # 是否无头启动浏览器，默认为否
        self.locator = locator  # 目标元素，当有xpath时这个元素用于相对检测
        self.logger = logger  # 日志对象
        self.operate_type = operate_type  # 操作方式，默认为js，用于点击、输入等操作
        self.page = page  # playwright运行的page对象
        self.xpath = xpath  # 元素定位的xpath
        self.wait_seconds = wait_seconds  # 等待时间，默认为120秒

    def info(self, message: str):
        if self.logger is None:
            return
        self.logger.info(message)

    def error(self, message: str):
        if self.logger is None:
            return
        self.logger.error(message)
