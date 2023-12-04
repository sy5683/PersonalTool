import abc

from selenium import webdriver


class LaunchBase(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def launch_browser(cls) -> webdriver:
        """启动浏览器"""

    @classmethod
    @abc.abstractmethod
    def close_browser(cls, driver: webdriver):
        """关闭浏览器"""
