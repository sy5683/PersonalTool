import typing

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .selenium_utils.control_browser.control_browser import ControlBrowser
from .selenium_utils.control_browser.download_driver import DownloadDriver
from .selenium_utils.control_browser.launch_chrome import LaunchChrome
from .selenium_utils.control_html.control_driver import ControlDriver
from .selenium_utils.control_html.control_element import ControlElement
from .selenium_utils.control_html.control_iframe import ControlIframe
from .selenium_utils.control_html.control_window import ControlWindow


class SeleniumUtil:

    @staticmethod
    def click(element_or_xpath: typing.Union[WebElement, str], **kwargs):
        """模拟点击"""
        ControlElement.click(element_or_xpath, **kwargs)

    @staticmethod
    def close_other_window(window_titles: typing.Union[str, typing.List[str]], **kwargs):
        """关闭其他窗口"""
        ControlWindow.close_other_window(window_titles, **kwargs)

    @staticmethod
    def close_browser(**kwargs):
        """关闭浏览器"""
        ControlBrowser.close_browser(**kwargs)

    @staticmethod
    def confirm_alert(**kwargs):
        """确定alert弹窗"""
        ControlWindow.confirm_alert(**kwargs)

    @staticmethod
    def execute_js(js: str, **kwargs):
        """执行js代码"""
        ControlDriver.execute_js(js, **kwargs)

    @staticmethod
    def exist(xpath: str, **kwargs) -> bool:
        """查找元素"""
        return ControlElement.exist(xpath, **kwargs)

    @staticmethod
    def find(xpath: str, **kwargs) -> WebElement:
        """查找元素"""
        return ControlElement.find(xpath, **kwargs)

    @staticmethod
    def finds(xpath: str, **kwargs) -> typing.List[WebElement]:
        """查找元素列表"""
        return ControlElement.finds(xpath, **kwargs)

    @staticmethod
    def get_chrome_driver_path() -> str:
        """获取chrome_driver路径"""
        return DownloadDriver.get_chrome_driver_path()

    @staticmethod
    def get_driver(**kwargs) -> WebDriver:
        """获取driver"""
        return ControlBrowser.get_driver(**kwargs)

    @staticmethod
    def input(element_or_xpath: typing.Union[WebElement, str], value: typing.Union[float, str], **kwargs):
        """输入"""
        ControlElement.input(element_or_xpath, str(value), **kwargs)

    @staticmethod
    def key_press(key_name: str = Keys.ENTER, **kwargs):
        """模拟按键"""
        ControlElement.key_press(key_name, **kwargs)

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

    @staticmethod
    def switch_window(window_title: str, **kwargs):
        """切换窗口"""
        ControlWindow.switch_window(window_title, **kwargs)
