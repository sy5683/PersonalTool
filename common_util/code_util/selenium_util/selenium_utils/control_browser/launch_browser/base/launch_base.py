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
        # 1) 先设置浏览器最小化
        try:
            driver.minimize_window()
        except common.exceptions.WebDriverException:
            time.sleep(0.5)
        # 2) 再设置浏览器最大化
        for _ in range(3):
            try:
                driver.maximize_window()
                break
            except common.exceptions.WebDriverException:
                time.sleep(0.5)
