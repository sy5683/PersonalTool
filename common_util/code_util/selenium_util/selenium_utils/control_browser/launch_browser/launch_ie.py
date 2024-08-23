import logging
import typing

import win32api
import win32con
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.ie.webdriver import WebDriver

from .base.launch_base import LaunchBase
from .download_driver import DownloadDriver
from ...selenium_config import SeleniumConfig


class LaunchIe(LaunchBase):
    _driver: typing.Union[WebDriver, None] = None

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        if cls._driver is None:
            # 1) 启动IE浏览器需要初始化其对应的参数与缩放比例
            cls._set_ie_setting()
            # 2) 启动IE浏览器
            cls._driver = cls._launch_ie(**kwargs)
            # 3.1) 设置默认加载超时时间
            cls._driver.set_page_load_timeout(SeleniumConfig.wait_seconds)
            # 3.2) 启动后设置浏览器最前端
            cls.set_browser_front(cls._driver)
        return cls._driver

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭IE浏览器"""
        driver = kwargs.get("driver", cls._driver)
        if driver is not None:
            # 使用selenium自带的quit方法关闭driver
            driver.quit()
            if driver == cls._driver:
                cls._driver = None

    @staticmethod
    def _set_ie_setting():
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""

        def __set_regedit_value(regedit_path: str, regedit_key: str, regedit_value: int):
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, regedit_path, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, regedit_key, 0, win32con.REG_DWORD, regedit_value)
            win32api.RegCloseKey(key)

        # 1) 设置浏览器缩放为100%
        __set_regedit_value("Software\\Microsoft\\Internet Explorer\\Zoom", "ZoomFactor", 100000)
        # 2) 设置浏览器所有保护模式统一开启或关闭
        for each in range(1, 5):
            # 最后一个参数: 0: 开启, 3: 关闭
            __set_regedit_value(f"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\{each}",
                                "2500", 3)

    @staticmethod
    def _launch_ie(**kwargs) -> WebDriver:
        """启动IE浏览器"""
        logging.info("启动IE浏览器")
        # 2.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 2.2) IE浏览器无法设置静默运行
        # 2.3) 设置ip代理
        if SeleniumConfig.proxy_ip:
            options.add_argument(f"--proxy-server={SeleniumConfig.proxy_ip}")
        # 2.4) 设置忽略私密链接警告，但IE驱动程序不允许绕过不安全(自签名)SSL证书，因此这个方法相当于无效
        # options.set_capability("acceptInsecureCerts", True)
        # 3) 启动IE浏览器
        driver_path = kwargs.get("driver_path", DownloadDriver.get_ie_driver_path())
        service = Service(executable_path=driver_path)
        return webdriver.Ie(options=options, service=service)
