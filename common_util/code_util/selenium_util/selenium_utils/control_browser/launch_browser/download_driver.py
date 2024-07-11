import logging
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import DEFAULT_USER_HOME_CACHE_PATH
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager


class DownloadDriver:

    @classmethod
    def get_chrome_driver_path(cls) -> str:
        """获取chrome_driver路径"""
        chrome_driver_manager = ChromeDriverManager()
        try:
            # 1) 获取谷歌浏览器版本
            chrome_version = chrome_driver_manager.driver.get_browser_version_from_os()
            logging.info(f"Chrome浏览器版本: {chrome_version}")
            # 2) 根据默认下载路径遍历文件，获取指定版本的chrome_driver文件
            return cls.__get_driver_in_manager_path("chromedriver.exe", chrome_version)
        except FileExistsError:
            # 3) 未找到指定版本的chrome_driver文件，则调用下载方法
            return chrome_driver_manager.install()

    @classmethod
    def get_edge_driver_path(cls) -> str:
        """获取edge_driver路径"""
        edge_driver_manager = EdgeChromiumDriverManager()
        try:
            # 1) 获取Edge浏览器版本
            edge_version = edge_driver_manager.driver.get_browser_version_from_os()
            logging.info(f"Edge浏览器版本: {edge_version}")
            # 2) 根据默认下载路径遍历文件，获取指定版本的edge_driver文件
            return cls.__get_driver_in_manager_path("msedgedriver.exe", edge_version)
        except FileExistsError:
            # 3) 未找到指定版本的edge_driver文件，则调用下载方法
            return edge_driver_manager.install()

    @classmethod
    def get_ie_driver_path(cls) -> str:
        """获取ie_driver路径"""
        try:
            # 1) 根据默认下载路径遍历文件，获取ie_driver文件
            return cls.__get_driver_in_manager_path("IEDriverServer.exe")
        except FileExistsError:
            # 2) 未找到指定版本的chrome_driver文件，则调用下载方法
            return IEDriverManager().install()

    @staticmethod
    def __get_driver_in_manager_path(driver_name: str, check_version: str = '') -> str:
        """从获取DriverManager下载路径中获取driver"""
        if "." in check_version:
            check_version = check_version[:check_version.find(".")]
        for driver_path in Path(DEFAULT_USER_HOME_CACHE_PATH).rglob(driver_name):
            if check_version and check_version not in str(driver_path):
                continue
            return str(driver_path)
        raise FileExistsError
