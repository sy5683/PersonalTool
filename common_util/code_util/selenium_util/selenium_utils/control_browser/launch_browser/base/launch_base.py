import abc
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver


class LaunchBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_driver(self, **kwargs) -> WebDriver:
        """获取driver"""

    @abc.abstractmethod
    def close_browser(self, **kwargs):
        """关闭浏览器"""

    @staticmethod
    def set_browser_front(driver: webdriver):
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
