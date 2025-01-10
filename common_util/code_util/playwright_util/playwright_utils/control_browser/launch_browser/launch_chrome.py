import subprocess
import threading
import typing

from playwright.sync_api import *

from .base.launch_base import LaunchBase
from ...entity.playwright_config import PlaywrightConfig


class LaunchChrome(LaunchBase):
    _playwright = None
    _driver_map: typing.Dict[int, typing.Tuple[Browser, BrowserContext, Page]] = {}

    @classmethod
    def close_browser(cls, playwright_config: PlaywrightConfig):
        """关闭浏览器"""

    @classmethod
    def get_driver(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """获取句柄browser, context, page"""
        # 1) 返回参数中传入的browser, context, page
        if playwright_config.browser:
            return playwright_config.browser, playwright_config.context, playwright_config.page
        # 2) 获取debug端口
        debug_port = cls.__get_debug_port(playwright_config)
        # 3.1) 获取进程id，并启动谷歌浏览器
        if debug_port is None:
            thread_id = threading.current_thread().ident
            if thread_id not in cls._driver_map:
                cls._driver_map[thread_id] = cls._launch_chrome(playwright_config)
            return cls._driver_map[thread_id]
        # 3.2) 使用debug方式接管谷歌浏览器
        else:
            if debug_port not in cls._driver_map:
                cls._driver_map[debug_port] = cls._take_over_chrome(playwright_config)
            return cls._driver_map[debug_port]

    @classmethod
    def _launch_chrome(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """启动谷歌浏览器"""
        playwright_config.info("启动谷歌浏览器")
        playwright = cls.__create_playwright()

    @classmethod
    def _take_over_chrome(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """接管谷歌浏览器"""
        debug_port = cls.__get_debug_port(playwright_config)
        assert cls.__netstat_debug_port_running(debug_port), f"当前端口并未启动，无法接管谷歌浏览器: {debug_port}"
        playwright_config.info(f"接管已debug运行的谷歌浏览器，端口: {debug_port}")
        playwright = cls.__create_playwright()

    @classmethod
    def __create_playwright(cls) -> Playwright:
        """生成playwright实例对象"""
        if cls._playwright is None:
            cls._playwright = sync_playwright().start()
        return cls._playwright

    @classmethod
    def __get_debug_port(cls, playwright_config: PlaywrightConfig,
                         return_default: bool = False) -> typing.Union[int, None]:
        """获取debug端口"""
        # 1) 获取参数中的debug_port
        if playwright_config.debug_port:
            return playwright_config.debug_port
        # 2) 返回默认的debug_port
        default_debug_port = 9222
        # 2.1) 如果需要返回默认的debug_port，则无需进行判断debug_port是否正在运行，直接返回
        if return_default:
            return default_debug_port
        # 2.2) 检测默认的debug_port是否正在运行，如果正在运行，则返回默认的debug_port
        if cls.__netstat_debug_port_running(default_debug_port):
            return default_debug_port
        # 3) 返回空值
        return None

    @staticmethod
    def __netstat_debug_port_running(debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        # noinspection PyBroadException
        try:
            cmd = f'netstat -ano | findstr "{debug_port}" | findstr "LISTEN"'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(debug_port) in p.stdout.read()
        except Exception:
            return False
