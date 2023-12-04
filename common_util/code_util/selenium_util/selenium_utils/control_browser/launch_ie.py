import logging

import win32api
import win32con
from selenium import webdriver
from selenium.webdriver.ie.service import Service

from .download_driver import DownloadDriver
from .launch_base import LaunchBase
from ..selenium_config import SeleniumConfig


class LaunchIe(LaunchBase):

    @classmethod
    def launch_browser(cls) -> webdriver:
        """启动IE浏览器"""
        logging.info("启动IE浏览器")
        # 1) 启动IE浏览器需要初始化其对应的参数与缩放比例
        cls._set_ie_setting()
        # 2.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 2.2) IE浏览器无法设置静默运行
        # 2.3) 设置ip代理
        if SeleniumConfig.proxy_ip:
            options.add_argument(f"--proxy-server={SeleniumConfig.proxy_ip}")
        # 2.4) 设置忽略私密链接警告，但IE驱动程序不允许绕过不安全(自签名)SSL证书，因此这个方法相当于无效
        # options.set_capability("acceptInsecureCerts", True)
        # 3) 启动IE浏览器
        return cls.__launch_ie_driver(options)

    @classmethod
    def close_browser(cls, driver: webdriver):
        """关闭IE浏览器"""
        if driver is None:
            return
        driver.quit()

    @classmethod
    def _set_ie_setting(cls):
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""
        # 1.1) 设置浏览器缩放为100%
        cls.__set_regedit_value("Software\\Microsoft\\Internet Explorer\\Zoom", "ZoomFactor", 100000)
        # 1.2) 设置浏览器所有保护模式统一开启或关闭
        for each in range(1, 5):
            # 最后一个参数: 0: 开启, 3: 关闭
            regedit_path = f"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\{each}"
            cls.__set_regedit_value(regedit_path, "2500", 3)

    @staticmethod
    def __launch_ie_driver(options: webdriver.IeOptions) -> webdriver:
        """启动IE浏览器"""
        driver_path = DownloadDriver.get_ie_driver_path()
        service = Service(executable_path=driver_path)
        return webdriver.Ie(options=options, service=service)

    @staticmethod
    def __set_regedit_value(regedit_path: str, regedit_key: str, regedit_value: int):
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, regedit_path, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, regedit_key, 0, win32con.REG_DWORD, regedit_value)
        win32api.RegCloseKey(key)
