import logging
import os
import re
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver, common
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.ie.service import Service as IeService

from .base.launch_base import LaunchBase
from .download_driver import DownloadDriver
from ...selenium_config import SeleniumConfig


class LaunchEdge(LaunchBase):
    _driver: typing.Union[WebDriver, None] = None

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        if cls._driver is None:
            # 1) 启动Edge浏览器
            cls._driver = cls._launch_edge()
            # 2.1) 设置默认加载超时时间
            cls._driver.set_page_load_timeout(SeleniumConfig.wait_seconds)
            # 2.2) 启动后设置浏览器最前端
            cls.set_browser_front(cls._driver)
        return cls._driver

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭Edge浏览器"""
        driver = kwargs.get("driver", cls._driver)
        if driver is not None:
            # 使用selenium自带的quit方法关闭driver
            driver.quit()
            if driver == cls._driver:
                cls._driver = None

    @classmethod
    def _launch_edge(cls) -> WebDriver:
        """启动Edge浏览器"""
        logging.info("启动Edge浏览器")
        try:
            # 1.1) 获取Edge浏览器用户缓存路径
            user_data_dir = cls._get_edge_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_edge_driver(user_data_dir=user_data_dir)
        except common.InvalidArgumentException:
            # 1.3) 重新获取driver，不加载user_data_dir
            driver = cls._get_edge_driver()
        return driver

    @classmethod
    def _launch_edge_with_ie(cls) -> WebDriver:
        """ie模式启动Edge浏览器"""
        logging.info("ie模式启动Edge浏览器")
        # 1.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 1.2) IE浏览器无法设置静默运行
        # 1.3) 设置ip代理
        if SeleniumConfig.proxy_ip:
            options.add_argument(f"--proxy-server={SeleniumConfig.proxy_ip}")
        # 1.4) 使用edge启动
        options.attach_to_edge_chrome = True
        options.edge_executable_path = cls._get_edge_path()
        # 2) 启动IE浏览器
        driver_path = DownloadDriver.get_ie_driver_path()
        service = IeService(executable_path=driver_path)
        return webdriver.Ie(options=options, service=service)

    @staticmethod
    def _get_edge_driver(user_data_dir: str = None) -> WebDriver:
        """获取edge_driver"""
        # 1.1) 获取Edge浏览器设置
        options = webdriver.EdgeOptions()
        # 1.2) 设置静默运行
        if SeleniumConfig.headless:
            options.add_argument('--headless')
        # 1.3) 设置ip代理
        if SeleniumConfig.proxy_ip:
            options.add_argument(f"--proxy-server={SeleniumConfig.proxy_ip}")
        # 1.4) 设置忽略私密链接警告
        options.add_argument('--ignore-certificate-errors')
        # 1.5) 设置取消提示受自动控制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 取消提示和默认下载路径在同一个参数中配置
        prefs = options.experimental_options.get("prefs", {})
        # 1.6) 设置取消提示
        prefs.update({'credentials_enable_service': False})  # 设置取消提示保存密码
        prefs.update({'download.prompt_for_download': False})  # 取消提示下载
        # 1.7) 设置默认下载路径
        logging.info(f"浏览器下载路径为: {SeleniumConfig.download_path}")
        if os.path.exists(SeleniumConfig.download_path):
            prefs.update({'download.default_directory': SeleniumConfig.download_path})
        options.add_experimental_option('prefs', prefs)
        # 1.8) 设置读取用户缓存目录
        if user_data_dir and os.path.exists(user_data_dir):
            options.add_argument(f"--user-data-dir={user_data_dir}")
        # 2) 启动Edge浏览器
        driver_path = DownloadDriver.get_edge_driver_path()
        service = EdgeService(executable_path=driver_path)
        return webdriver.Edge(options=options, service=service)

    @staticmethod
    def _get_edge_path() -> str:
        """获取Edge浏览器路径"""
        # 1) 通过注册表查找Edge浏览器路径
        for regedit_dir in [win32con.HKEY_LOCAL_MACHINE, win32con.HKEY_CURRENT_USER]:  # Edge浏览器路径注册表一般在这两个位置下固定位置
            regedit_path = "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\msedge.exe"
            try:
                key = win32api.RegOpenKey(regedit_dir, regedit_path)
                edge_path, _ = win32api.RegQueryValueEx(key, "path")
            except pywintypes.error:
                continue
            edge_path = os.path.join(edge_path, "msedge.exe")
            if os.path.isfile(edge_path):
                return edge_path
        # 2) 通过遍历Edge浏览器常用安装路径查找Edge浏览器路径
        for edge_parent_path in [os.path.join(os.path.expanduser('~'), "AppData\\Local"), "C:\\Program Files",
                                 "C:\\Program Files (x86)"]:
            edge_path = os.path.join(edge_parent_path, "Microsoft\\Edge\\Application\\msedge.exe")
            if os.path.isfile(edge_path):
                return edge_path
        # 3) 某些极个别特殊情况，用户直接解压绿色文件使用Edge浏览器，这时候注册表没值路径也不确定，因此只能遍历全部文件路径
        for root_path in re.findall(r"(.:\\)", win32api.GetLogicalDriveStrings()):
            # 使用pathlib的rglob遍历，比for循环遍历更快，代码更简单
            for edge_path in Path(root_path).rglob("msedge.exe"):
                return str(edge_path)
        raise FileExistsError("未找到Edge浏览器路径")

    @staticmethod
    def _get_edge_user_data_path() -> typing.Union[str, None]:
        """获取Edge浏览器用户缓存User Data路径"""
        # 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        return None
