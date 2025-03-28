import abc
import os
import threading
import time
import typing

from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver

from ..base.launch_base import LaunchBase
from ..download_driver import DownloadDriver
from ....entity.selenium_config import SeleniumConfig


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
    @abc.abstractmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        return cls.__get_subclass().get_driver(selenium_config)

    @staticmethod
    def _get_driver_path(selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 1) 使用参数中的driver_path
        if selenium_config.driver_path:
            return selenium_config.driver_path
        # 2) 自动获取下载的driver_path路径
        return DownloadDriver.get_ie_driver_path()

    @classmethod
    @abc.abstractmethod
    def _set_ie_setting(cls):
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""
        cls.__get_subclass()._set_ie_setting()

    @classmethod
    def _launch_ie(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动IE浏览器"""
        selenium_config.info("启动IE浏览器")
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
        driver_path = cls._get_driver_path(selenium_config)
        from selenium.webdriver.ie.service import Service
        return webdriver.Ie(options=options, service=Service(executable_path=driver_path))

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .launch_ie_windows import LaunchIeWindows
            return LaunchIeWindows
        elif os.name == "posix":
            from .launch_ie_linux import LaunchIeLinux
            return LaunchIeLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
