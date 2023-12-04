import logging
import os
import re
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IeService

from common_core.base.exception_base import FileFindError
from .download_driver import DownloadDriver
from .launch_base import LaunchBase
from ..selenium_config import SeleniumConfig


class LaunchEdge(LaunchBase):

    @classmethod
    def launch_browser(cls) -> webdriver:
        """启动Edge浏览器"""
        logging.info("启动Edge浏览器")
        try:
            # 1.1) 获取Edge浏览器用户缓存路径
            user_data_dir = cls._get_edge_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_edge_driver(user_data_dir=user_data_dir)
        except InvalidArgumentException:
            # 1.3) 重新获取driver，不加载user_data_dir
            driver = cls._get_edge_driver()
        return driver

    @classmethod
    def launch_edge_with_ie(cls) -> webdriver:
        """ie模式启动Edge浏览器"""
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

    @classmethod
    def close_browser(cls, driver: webdriver):
        """关闭Edge浏览器"""
        if driver is None:
            return
        driver.quit()

    @classmethod
    def _get_edge_driver(cls, user_data_dir: str = None) -> webdriver:
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
        return cls.__launch_edge_driver(options)

    @classmethod
    def _get_edge_path(cls) -> str:
        """获取Edge浏览器路径"""
        # 1) 通过注册表查找Edge浏览器路径
        for regedit_dir in [win32con.HKEY_LOCAL_MACHINE, win32con.HKEY_CURRENT_USER]:  # 谷歌浏览器路径注册表一般在这两个位置下固定位置
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
        # 3) 某些极个别特殊情况，用户直接解压绿色文件使用谷歌浏览器，这时候注册表没值路径也不确定，因此只能遍历全部文件路径
        for root_path in re.findall(r"(.:\\)", win32api.GetLogicalDriveStrings()):
            # 使用pathlib的rglob遍历，比for循环遍历更快，代码更简单
            for edge_path in Path(root_path).rglob("msedge.exe"):
                return str(edge_path)
        raise FileFindError("未找到谷歌浏览器路径")

    @classmethod
    def _get_edge_user_data_path(cls) -> typing.Union[str, None]:
        """获取Edge浏览器用户缓存User Data路径"""
        # 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        return None

    @staticmethod
    def __launch_edge_driver(options: webdriver.EdgeOptions) -> webdriver:
        """启动Edge浏览器"""
        driver_path = DownloadDriver.get_edge_driver_path()
        service = EdgeService(executable_path=driver_path)
        return webdriver.Edge(options=options, service=service)
