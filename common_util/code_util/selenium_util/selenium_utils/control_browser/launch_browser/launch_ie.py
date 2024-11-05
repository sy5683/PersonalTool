import logging
import threading
import time
import typing

import win32con
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.ie.webdriver import WebDriver
from win32api import RegCloseKey, RegOpenKey, RegSetValueEx

from .base.launch_base import LaunchBase
from .download_driver import DownloadDriver
from ...entity.selenium_config import SeleniumConfig


class LaunchIe(LaunchBase):
    _driver_map: typing.Dict[int, WebDriver] = {}

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭IE浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        driver = selenium_config.driver
        if driver is None:
            driver = cls._driver_map.get(threading.current_thread().ident)
        if driver is None:
            return
        # 2) 使用selenium自带的quit方法关闭driver
        driver.quit()
        time.sleep(1)  # 等待一秒，确认等待操作执行完成
        # 3) 清除缓存
        selenium_config.driver = None
        for key, _driver in list(cls._driver_map.items()):
            if driver == _driver:
                del cls._driver_map[key]

    @classmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        # 1) 返回参数中传入的driver
        if selenium_config.driver:
            return selenium_config.driver
        # 2) 启动IE浏览器需要初始化其对应的参数与缩放比例
        cls._set_ie_setting()
        # 3) 获取进程id，并启动IE浏览器
        thread_id = threading.current_thread().ident
        if thread_id not in cls._driver_map:
            cls._driver_map[thread_id] = cls._launch_ie(selenium_config)
        return cls._driver_map[thread_id]

    @staticmethod
    def _set_ie_setting():
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""

        def set_regedit_value(regedit_path: str, regedit_key: str, regedit_value: int):
            key = RegOpenKey(win32con.HKEY_CURRENT_USER, regedit_path, 0, win32con.KEY_ALL_ACCESS)
            RegSetValueEx(key, regedit_key, 0, win32con.REG_DWORD, regedit_value)
            RegCloseKey(key)

        # 1) 设置浏览器缩放为100%
        set_regedit_value("Software\\Microsoft\\Internet Explorer\\Zoom", "ZoomFactor", 100000)
        # 2) 设置浏览器所有保护模式统一开启或关闭
        for each in range(1, 5):
            # 最后一个参数: 0->开启, 3->关闭
            set_regedit_value(f"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\{each}", "2500",
                              3)

    @classmethod
    def _launch_ie(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动IE浏览器"""
        logging.info("启动IE浏览器")
        # 1.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 1.2.1) IE浏览器无法设置静默运行
        # 1.2.2) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3.1) 设置忽略私密链接警告，但IE驱动程序不允许绕过不安全(自签名)SSL证书，因此这个方法相当于无效
        # options.set_capability("acceptInsecureCerts", True)
        # 2) 启动IE浏览器
        driver = cls._launch_ie_driver(selenium_config, options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    def _launch_ie_driver(cls, selenium_config: SeleniumConfig, options: webdriver.IeOptions) -> WebDriver:
        """启动IE浏览器driver"""
        driver_path = cls.__get_driver_path(selenium_config)
        service = Service(executable_path=driver_path)
        return webdriver.Ie(options=options, service=service)

    @staticmethod
    def __get_driver_path(selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 1) 使用参数中的driver_path
        if selenium_config.driver_path:
            return selenium_config.driver_path
        # 2) 自动获取下载的driver_path路径
        return DownloadDriver.get_ie_driver_path()
