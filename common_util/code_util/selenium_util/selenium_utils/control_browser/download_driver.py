import logging
from pathlib import Path

import win32api
import win32con
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import DEFAULT_USER_HOME_CACHE_PATH
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager


class DownloadDriver:

    @classmethod
    def get_chrome_driver_path(cls) -> str:
        """获取chrome_driver路径"""
        # 1) 获取谷歌浏览器版本与目标chrome_driver版本
        chrome_version = cls._get_browser_version("Software\\Google\\Chrome\\BLBeacon")
        logging.info(f"Chrome浏览器版本: {chrome_version}")
        # 2.1) 根据默认下载路径遍历文件，获取指定版本的chrome_driver文件
        try:
            return cls._get_driver_in_manager_path("chromedriver.exe", chrome_version)
        except FileExistsError:
            # 2.2) 未找到指定版本的chrome_driver文件，则调用下载方法
            return ChromeDriverManager().install()

    @classmethod
    def get_edge_driver_path(cls) -> str:
        """获取edge_driver路径"""
        # 1) 获取Edge浏览器版本与目标edge_driver版本
        edge_version = cls._get_browser_version("Software\\Microsoft\\Edge\\BLBeacon")
        logging.info(f"Edge浏览器版本: {edge_version}")
        # 2.1) 根据默认下载路径遍历文件，获取指定版本的edge_driver文件
        try:
            return cls._get_driver_in_manager_path("msedgedriver.exe", edge_version)
        except FileExistsError:
            # 2.2) 未找到指定版本的edge_driver文件，则调用下载方法
            return EdgeChromiumDriverManager().install()

    @classmethod
    def get_ie_driver_path(cls) -> str:
        """获取ie_driver路径"""
        # 1) 根据默认下载路径遍历文件，获取ie_driver文件
        try:
            return cls._get_driver_in_manager_path("IEDriverServer.exe")
        except FileExistsError:
            # 2) 未找到指定版本的chrome_driver文件，则调用下载方法
            return IEDriverManager().install()

    @staticmethod
    def _get_browser_version(regedit_path: str) -> str:
        """获取注册表的值"""
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, regedit_path)
        value, key_type = win32api.RegQueryValueEx(key, "version")
        return value

    @staticmethod
    def _get_driver_in_manager_path(driver_name: str, check_version: str = '') -> str:
        """从获取DriverManager下载路径中获取driver"""
        if "." in check_version:
            check_version = check_version[:check_version.find(".")]
        for driver_path in Path(DEFAULT_USER_HOME_CACHE_PATH).rglob(driver_name):
            if check_version and check_version not in str(driver_path):
                continue
            return str(driver_path)
        raise FileExistsError
