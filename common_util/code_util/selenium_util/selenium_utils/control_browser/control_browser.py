import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver

from .browser_type import BrowserType
from .launch_chrome import LaunchChrome
from .launch_edge import LaunchEdge
from .launch_ie import LaunchIe
from ..selenium_config import SeleniumConfig


class ControlBrowser:
    _driver = None

    @classmethod
    def get_driver(cls) -> WebDriver:
        """获取driver"""
        if cls._driver is None:
            # 1) 启动浏览器
            cls._driver = cls.__get_driver_launch().launch_browser()
            # 2.1) 设置默认加载超时时间
            cls._driver.set_page_load_timeout(SeleniumConfig.wait_seconds)
            # 2.2) 设置窗口最前端
            cls._set_browser_front(cls._driver)
        return cls._driver

    @classmethod
    def close_browser(cls):
        """关闭谷歌浏览器"""
        if cls._driver is None:
            return
        cls.__get_driver_launch().close_browser(cls._driver)
        cls._driver = None

    @staticmethod
    def __get_driver_launch():
        if SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchChrome
        elif SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchEdge
        elif SeleniumConfig.browser_type == BrowserType.chrome:
            return LaunchIe
        else:
            raise TypeError(f"暂不支持的浏览器类型: {SeleniumConfig.browser_type.name}")

    @staticmethod
    def _set_browser_front(driver: webdriver):
        """设置浏览器最前端"""
        try:  # 先设置浏览器最小化
            driver.minimize_window()
        except WebDriverException:
            pass  # 设置最小化时可能会因为正在操作而失败
        for _ in range(3):
            try:  # 再设置浏览器最大化
                driver.maximize_window()
                break
            except WebDriverException:
                # 设置最大化时可能会因为正在操作而失败
                time.sleep(0.5)
