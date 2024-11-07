from selenium.webdriver.ie.webdriver import WebDriver

from .launch_ie import LaunchIe


class LaunchIeLinux(LaunchIe):

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        raise FileExistsError("Linux系统中不存在IE浏览器。")

    @classmethod
    def _set_ie_setting(cls):
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""
        raise FileExistsError("Linux系统中不存在IE浏览器。")
