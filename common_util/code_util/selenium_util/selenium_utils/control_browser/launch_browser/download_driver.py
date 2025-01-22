import logging
import os
import re
import traceback
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import DEFAULT_USER_HOME_CACHE_PATH
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager


class DownloadDriver:

    @classmethod
    def get_chrome_version(cls) -> str:
        """获取谷歌浏览器版本"""
        return ChromeDriverManager().driver.get_browser_version_from_os()

    @classmethod
    def get_edge_version(cls) -> str:
        """获取Edge浏览器版本"""
        return EdgeChromiumDriverManager().driver.get_browser_version_from_os()

    @classmethod
    def get_chrome_driver_path(cls) -> str:
        """获取chrome_driver路径"""
        # 1) 获取谷歌浏览器版本
        chrome_version = cls.get_chrome_version()
        logging.info(f"谷歌浏览器版本: {chrome_version}")
        if chrome_version is None:
            raise FileExistsError("未安装谷歌浏览器")
        # 2) 根据默认下载路径遍历文件，获取指定版本的chrome_driver文件
        driver_name = "chromedriver.exe" if os.name == "nt" else "chromedriver"
        try:
            return cls._get_driver_in_manager_path(driver_name, chrome_version)
        except FileExistsError:
            logging.warning("本地缓存中没有指定版本的谷歌浏览器驱动")
        # 3) 未找到指定版本的chrome_driver文件，则调用下载方法
        try:
            return os.path.join(os.path.dirname(ChromeDriverManager().install()), driver_name)
        except ConnectionError:
            logging.warning(f"webdriver_manager下载谷歌浏览器驱动失败: {traceback.format_exc()}")
        raise ConnectionError("谷歌浏览器驱动下载失败")

    @classmethod
    def get_edge_driver_path(cls) -> str:
        """获取edge_driver路径"""
        # 1) 获取Edge浏览器版本
        edge_version = cls.get_edge_version()
        logging.info(f"Edge浏览器版本: {edge_version}")
        if edge_version is None:
            raise FileExistsError("未安装Edge浏览器")
        # 2) 根据默认下载路径遍历文件，获取指定版本的edge_driver文件
        driver_name = "msedgedriver.exe" if os.name == "nt" else "msedgedriver"
        try:
            return cls._get_driver_in_manager_path(driver_name, edge_version)
        except FileExistsError:
            logging.warning("本地缓存中没有指定版本的Edge浏览器驱动")
        # 3) 未找到指定版本的edge_driver文件，则调用下载方法
        try:
            return os.path.join(os.path.dirname(EdgeChromiumDriverManager().install()), driver_name)
        except ConnectionError:
            logging.warning(f"webdriver_manager下载Edge浏览器驱动失败: {traceback.format_exc()}")
        raise ConnectionError("Edge浏览器驱动下载失败")

    @classmethod
    def get_ie_driver_path(cls) -> str:
        """获取ie_driver路径"""
        # 1) 根据默认下载路径遍历文件，获取ie_driver文件
        driver_name = "IEDriverServer.exe" if os.name == "nt" else "IEDriverServer"
        try:
            return cls._get_driver_in_manager_path(driver_name)
        except FileExistsError:
            logging.warning("本地缓存中没有指定版本的IE浏览器驱动")
        # 2) 未找到指定版本的chrome_driver文件，则调用下载方法
        try:
            return os.path.join(os.path.dirname(IEDriverManager().install()), driver_name)
        except ConnectionError:
            logging.warning(f"webdriver_manager下载IE浏览器驱动失败: {traceback.format_exc()}")
        raise ConnectionError("IE浏览器驱动下载失败")

    @staticmethod
    def _get_driver_in_manager_path(driver_name: str, check_version: str = '') -> str:
        """从获取DriverManager下载路径中获取driver"""
        # 驱动只需要保证大版本一致即可
        check_version = check_version[:check_version.find(".")] if "." in check_version else check_version
        # 遍历驱动下载路径的指定文件
        driver_paths = list(Path(DEFAULT_USER_HOME_CACHE_PATH).rglob(driver_name))
        if not driver_paths:
            raise FileExistsError
        for driver_path in driver_paths:
            if driver_path.is_dir():
                continue
            relative_path = str(driver_path).replace(DEFAULT_USER_HOME_CACHE_PATH, "")
            if check_version and not re.search(rf"\\{check_version}\.|\\{check_version}\\", relative_path):
                continue
            return str(driver_path)
        raise FileExistsError(f"DriverManager下载路径没有指定版本driver: {check_version}")
