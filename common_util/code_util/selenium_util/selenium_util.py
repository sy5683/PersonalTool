from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from common_core.base.util_base import UtilBase
from .selenium_utils.control_browser.browser_type import BrowserType
from .selenium_utils.control_browser.control_browser import ControlBrowser
from .selenium_utils.control_html.control_element import ControlElement
from .selenium_utils.selenium_config import SeleniumConfig


class SeleniumUtil(UtilBase):

    @staticmethod
    def get_driver(wait_seconds: int = 120) -> webdriver:
        """获取driver"""
        return ControlBrowser.get_driver(wait_seconds)

    @classmethod
    def find_element(cls, xpath: str, wait_seconds: int = 120) -> WebElement:
        """查找元素"""
        return ControlElement.find_element(cls.get_driver(), xpath, wait_seconds)

    @classmethod
    def open_url(cls, url: str):
        """打开url"""
        cls.get_driver().get(url)

    @staticmethod
    def set_browser_type(browser_type: BrowserType):
        """设置浏览器类型"""
        SeleniumConfig.browser_type = browser_type

    @staticmethod
    def set_download_path(download_path: str):
        """设置浏览器下载路径"""
        SeleniumConfig.download_path = download_path

    @staticmethod
    def set_headless():
        """设置无头控制selenium"""
        SeleniumConfig.headless = True

    @staticmethod
    def set_proxy_ip(proxy_ip: str):
        """设置代理ip"""
        SeleniumUtil.proxy_ip = proxy_ip
