import typing

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .selenium_utils.control_browser.control_browser import ControlBrowser
from .selenium_utils.control_html.control_element import ControlElement
from .selenium_utils.control_html.control_iframe import ControlIframe
from .selenium_utils.selenium_config import SeleniumConfig


class SeleniumUtil:

    @staticmethod
    def close_browser():
        """关闭谷歌浏览器"""
        ControlBrowser.close_browser()

    @staticmethod
    def find_element(element: typing.Union[WebDriver, WebElement], xpath: str,
                     wait_seconds: int = SeleniumConfig.wait_seconds) -> WebElement:
        """查找元素"""
        return ControlElement.find_element(element, xpath, wait_seconds)

    @staticmethod
    def get_attribute(element: typing.Union[WebDriver, WebElement], xpath: str, parameter: str,
                      wait_seconds: int = SeleniumConfig.wait_seconds) -> str:
        """获取元素参数"""
        return ControlElement.get_attribute(element, xpath, parameter, wait_seconds)

    @staticmethod
    def get_driver() -> WebDriver:
        """获取driver"""
        return ControlBrowser.get_driver()

    @classmethod
    def open_url(cls, url: str):
        """打开url"""
        cls.get_driver().get(url)

    @classmethod
    def switch_iframe(cls, xpath: str, wait_seconds: int = SeleniumConfig.wait_seconds):
        """切换iframe"""
        ControlIframe.switch_iframe(cls.get_driver(), xpath, wait_seconds)
