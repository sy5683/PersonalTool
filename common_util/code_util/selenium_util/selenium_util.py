import typing

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .selenium_utils.control_browser.control_browser import ControlBrowser
from .selenium_utils.control_browser.launch_chrome import LaunchChrome
from .selenium_utils.control_html.control_element import ControlElement
from .selenium_utils.control_html.control_iframe import ControlIframe
from .selenium_utils.selenium_config import SeleniumConfig


class SeleniumUtil:

    @staticmethod
    def close_browser(**kwargs):
        """关闭浏览器"""
        ControlBrowser.close_browser(**kwargs)

    @staticmethod
    def find(xpath: str, **kwargs) -> WebElement:
        """查找元素"""
        return ControlElement.find(xpath, **kwargs)

    @staticmethod
    def finds(xpath: str, **kwargs) -> typing.List[WebElement]:
        """查找元素列表"""
        return ControlElement.finds(xpath, **kwargs)

    @staticmethod
    def get_driver(**kwargs) -> WebDriver:
        """获取driver"""
        return ControlBrowser.get_driver(**kwargs)

    @staticmethod
    def input(element_or_xpath: typing.Union[WebElement, str], value: str, need_check: bool, **kwargs):
        """输入"""
        ControlElement.input(element_or_xpath, value, need_check, **kwargs)

    @staticmethod
    def launch_chrome_debug(debug_port: int = None):
        """debug启动谷歌浏览器"""
        LaunchChrome.launch_browser_debug(debug_port)

    @classmethod
    def open_url(cls, url: str, **kwargs):
        """打开url"""
        cls.get_driver(**kwargs).get(url)

    @staticmethod
    def switch_iframe(element_or_xpath: typing.Union[WebElement, str] = '', **kwargs):
        """切换iframe"""
        ControlIframe.switch_iframe(element_or_xpath, **kwargs)
