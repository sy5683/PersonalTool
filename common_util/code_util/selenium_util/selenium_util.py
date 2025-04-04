import typing
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .selenium_utils.control_browser.control_browser import ControlBrowser
from .selenium_utils.control_browser.launch_browser.download_driver import DownloadDriver
from .selenium_utils.control_browser.launch_browser.launch_chrome.launch_chrome import LaunchChrome
from .selenium_utils.control_html.control_driver import ControlDriver
from .selenium_utils.control_html.control_element import ControlElement
from .selenium_utils.control_html.control_iframe import ControlIframe
from .selenium_utils.control_html.control_window import ControlWindow
from .selenium_utils.entity.selenium_config import SeleniumConfig


class SeleniumUtil:

    @staticmethod
    def click(selenium_config: SeleniumConfig):
        """模拟点击"""
        ControlElement.click(selenium_config)

    @staticmethod
    def close_other_window(selenium_config: SeleniumConfig, *window_titles: str):
        """关闭其他窗口"""
        ControlWindow.close_other_window(selenium_config, *window_titles)

    @staticmethod
    def close_browser(selenium_config: SeleniumConfig):
        """关闭浏览器"""
        ControlBrowser.close_browser(selenium_config)

    @staticmethod
    def confirm_alert(selenium_config: SeleniumConfig):
        """确定alert弹窗"""
        ControlWindow.confirm_alert(selenium_config)

    @staticmethod
    def execute_js(selenium_config: SeleniumConfig, js: str):
        """执行js代码"""
        ControlDriver.execute_js(selenium_config, js)

    @staticmethod
    def exist(selenium_config: SeleniumConfig) -> bool:
        """查找元素"""
        return ControlElement.exist(selenium_config)

    @staticmethod
    def find(selenium_config: SeleniumConfig) -> WebElement:
        """查找元素"""
        return ControlElement.find(selenium_config)

    @staticmethod
    def finds(selenium_config: SeleniumConfig) -> typing.List[WebElement]:
        """查找元素列表"""
        return ControlElement.finds(selenium_config)

    @staticmethod
    def get_action(selenium_config: SeleniumConfig) -> ActionChains:
        """获取模拟操作动作"""
        return ControlElement.get_action(selenium_config)

    @staticmethod
    def get_attribute(selenium_config: SeleniumConfig, attribute_type: str) -> str:
        """获取元素内容，常用的值有: id, class, value, innerText"""
        return ControlElement.get_attribute(selenium_config, attribute_type)

    @staticmethod
    def get_chrome_driver_path() -> str:
        """获取chrome_driver路径"""
        return DownloadDriver.get_chrome_driver_path()

    @staticmethod
    def get_driver(selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        return ControlBrowser.get_driver(selenium_config)

    @staticmethod
    def get_edge_driver_path() -> str:
        """获取edge_driver路径"""
        return DownloadDriver.get_edge_driver_path()

    @staticmethod
    def get_ie_driver_path() -> str:
        """获取ie_driver路径"""
        return DownloadDriver.get_ie_driver_path()

    @staticmethod
    def get_networks(selenium_config: SeleniumConfig) -> typing.List[dict]:
        """获取selenium运行中的network请求"""
        return ControlDriver.get_networks(selenium_config)

    @staticmethod
    def input(selenium_config: SeleniumConfig, value: typing.Union[float, str]):
        """输入"""
        ControlElement.input(selenium_config, str(value))

    @staticmethod
    def launch_chrome_debug(debug_port: int):
        """debug启动谷歌浏览器"""
        LaunchChrome.launch_browser_debug(SeleniumConfig(debug_port=debug_port))

    @staticmethod
    def open_url(selenium_config: SeleniumConfig, url: str):
        """打开url"""
        ControlDriver.open_url(selenium_config, url)

    @staticmethod
    def refresh(selenium_config: SeleniumConfig):
        """刷新"""
        ControlDriver.refresh(selenium_config)

    @staticmethod
    def screenshot(selenium_config: SeleniumConfig, save_path: typing.Union[Path, str] = None) -> str:
        """截图"""
        return ControlDriver.screenshot(selenium_config, save_path)

    @staticmethod
    def select(selenium_config: SeleniumConfig, value: typing.Union[int, str]):
        """选择下拉选项"""
        ControlElement.select(selenium_config, value)

    @staticmethod
    def switch_iframe(selenium_config: SeleniumConfig):
        """切换iframe"""
        ControlIframe.switch_iframe(selenium_config)

    @staticmethod
    def switch_window(selenium_config: SeleniumConfig, window_title: str):
        """切换窗口"""
        ControlWindow.switch_window(selenium_config, window_title)

    @staticmethod
    def wait_disappear(selenium_config: SeleniumConfig) -> bool:
        """等待元素消失"""
        return ControlElement.wait_disappear(selenium_config)
