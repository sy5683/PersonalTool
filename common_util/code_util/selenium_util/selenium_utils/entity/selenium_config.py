import logging
import typing

from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..enum.browser_type import BrowserType
from ..enum.operate_type import OperateType


class SeleniumConfig:

    def __init__(self,
                 browser_type: BrowserType = BrowserType.chrome,
                 check_input: bool = True,
                 close_task: bool = True,
                 debug_port: int = None,
                 download_path: typing.Union[str, Path] = "E:\\Download",
                 driver: WebDriver = None,
                 driver_path: typing.Union[str, Path] = None,
                 element: WebElement = None,
                 headless: bool = False,
                 operate_type: OperateType = OperateType.js,
                 proxy_ip: str = None,
                 use_user_data: bool = True,
                 user_data_dir: str = None,
                 xpath: str = '',
                 wait_seconds: int = 120,
                 without_log: bool = False
                 ):
        self.browser_type = browser_type  # 浏览器类型，默认为谷歌浏览器
        self.check_input = check_input  # 检测输入内容是否正确
        self.close_task = close_task  # 是否关闭浏览器cmd窗口
        self.debug_port = debug_port  # debug端口，用于接管浏览器
        self.download_path = download_path  # 浏览器下载路径
        self.driver = driver  # selenium运行的driver对象
        self.driver_path: str = str(driver_path) if driver_path else driver_path  # driver路径
        self.element = element  # 目标元素，当有xpath时这个元素用于相对检测
        self.headless = headless  # 是否无头启动浏览器，默认为否
        self.operate_type = operate_type  # 操作方式，主要有js、selenium，默认为js，用于点击
        self.proxy_ip = proxy_ip  # 代理ip
        self.use_user_data = use_user_data  # 浏览器启动是否使用user_data，默认为是
        self.user_data_dir = user_data_dir  # user_data目录
        self.xpath = xpath  # 元素定位的xpath
        self.wait_seconds = wait_seconds  # 等待时间，默认为120秒
        self.without_log = without_log  # 是否不打印日志

    def info(self, message: str):
        if self.without_log:
            return
        logging.info(message)
