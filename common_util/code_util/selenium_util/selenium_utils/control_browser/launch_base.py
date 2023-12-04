import abc

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class LaunchBase(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def launch_browser(cls) -> WebDriver:
        """启动浏览器"""

    @classmethod
    @abc.abstractmethod
    def close_browser(cls, driver: webdriver):
        """关闭浏览器"""
