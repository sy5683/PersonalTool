import abc
import time

from selenium import webdriver, common
from selenium.webdriver.chrome.webdriver import WebDriver

from ....entity.selenium_config import SeleniumConfig


class LaunchBase(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭浏览器"""

    @classmethod
    @abc.abstractmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""

    @staticmethod
    def set_browser_front(driver: webdriver):
        """设置浏览器最前端"""
        try:  # 先设置浏览器最小化
            driver.minimize_window()
        except common.WebDriverException:
            pass  # 设置最小化时可能会因为正在操作而失败
        for _ in range(3):
            try:  # 再设置浏览器最大化
                driver.maximize_window()
                break
            except common.WebDriverException:
                # 设置最大化时可能会因为正在操作而失败
                time.sleep(0.5)
