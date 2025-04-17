import logging
import pathlib
import typing

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..enum.browser_type import BrowserType
from ..enum.operate_type import OperateType
from ..selenium_cache import SeleniumCache


class SeleniumConfig:

    def __init__(self,
                 browser_type: BrowserType = BrowserType.chrome,
                 check_input: bool = True,
                 chrome_path: typing.Union[str, pathlib.Path] = None,
                 close_task: bool = True,
                 debug_port: int = None,
                 delay_seconds: int = 0,
                 download_path: typing.Union[str, pathlib.Path] = 'E:/Download',  # 默认值根据个人情况进行修改
                 driver: WebDriver = None,
                 driver_path: typing.Union[str, pathlib.Path] = None,
                 element: WebElement = None,
                 headless: bool = False,
                 logger: typing.Union[logging.Logger, None] = logging.getLogger(),
                 operate_type: OperateType = OperateType.js,
                 proxy_ip: str = None,
                 use_user_data: bool = True,
                 user_data_dir: typing.Union[str, pathlib.Path] = None,
                 xpath: str = '',
                 wait_seconds: int = 120,
                 ):
        self.browser_type = SeleniumCache.browser_type if browser_type is None else browser_type  # 浏览器类型，默认为谷歌浏览器
        SeleniumCache.browser_type = self.browser_type if self.browser_type != SeleniumCache.browser_type else SeleniumCache.browser_type
        self.check_input = check_input  # 检测输入内容是否正确
        self.chrome_path: str = str(chrome_path) if chrome_path else chrome_path  # 谷歌浏览器路径
        self.close_task = close_task  # 是否关闭浏览器cmd窗口
        self.debug_port = debug_port  # debug端口，用于接管浏览器
        self.delay_seconds = delay_seconds  # 演示时间，默认为0不等待
        self.download_path: str = str(download_path) if download_path else download_path  # 浏览器下载路径
        self.driver = driver  # selenium运行的driver对象
        self.driver_path: str = str(driver_path) if driver_path else driver_path  # driver路径
        self.element = element  # 目标元素，当有xpath时这个元素用于相对检测
        self.headless = headless  # 是否无头启动浏览器，默认为否
        self.logger = logger  # 日志对象
        self.operate_type = operate_type  # 操作方式，默认为js，用于点击、输入等操作
        self.proxy_ip = proxy_ip  # 代理ip
        self.use_user_data = use_user_data  # 浏览器启动是否使用user_data，默认为是
        self.user_data_dir = user_data_dir  # user_data目录
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
