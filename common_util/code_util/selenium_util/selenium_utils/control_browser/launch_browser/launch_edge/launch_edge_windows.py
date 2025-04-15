import os
import re
from pathlib import Path

import pywintypes
import win32con
from selenium.webdriver.edge.webdriver import WebDriver
from win32api import GetLogicalDriveStrings, RegOpenKey, RegQueryValueEx

from .launch_edge import LaunchEdge
from ....entity.selenium_config import SeleniumConfig


class LaunchEdgeWindows(LaunchEdge):

    @classmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        # 1) 返回参数中传入的driver
        if selenium_config.driver:
            cls._get_cache_driver(driver=selenium_config.driver)
            return selenium_config.driver
        # 2) 启动Edge浏览器
        cache_driver = cls._get_cache_driver()
        if cache_driver.driver is None:
            cache_driver.driver = cls._launch_edge(selenium_config)
        return cache_driver.driver

    @classmethod
    def _get_edge_path(cls) -> str:
        """获取Edge浏览器路径"""
        # 1) 通过注册表查找Edge浏览器路径
        for regedit_dir in [win32con.HKEY_LOCAL_MACHINE, win32con.HKEY_CURRENT_USER]:  # Edge浏览器路径注册表一般在这两个位置下固定位置
            regedit_path = os.path.join("Software", "Microsoft", "Windows", "CurrentVersion", "App Paths", "msedge.exe")
            try:
                key = RegOpenKey(regedit_dir, regedit_path)
                edge_path, _ = RegQueryValueEx(key, "path")
            except (pywintypes.error, FileNotFoundError, PermissionError, WindowsError, ValueError, TypeError):
                continue
            edge_path = os.path.join(edge_path, "msedge.exe")
            if os.path.isfile(edge_path):
                return edge_path
        # 2) 通过遍历Edge浏览器常用安装路径查找Edge浏览器路径
        for edge_parent_path in [os.path.join(os.path.expanduser('~'), "AppData", "Local"),
                                 os.path.join("C:/", "Program Files"),
                                 os.path.join("C:/", "Program Files (x86)")]:
            edge_path = os.path.join(edge_parent_path, "Microsoft", "Edge", "Application", "msedge.exe")
            if os.path.isfile(edge_path):
                return edge_path
        # 3) 某些极个别特殊情况，用户直接解压绿色文件使用Edge浏览器，这时候注册表没值路径也不确定，因此只能遍历全部文件路径
        for root_path in re.findall(r"(.:/)", GetLogicalDriveStrings()):
            for edge_path in Path(root_path).rglob("msedge.exe"):
                return str(edge_path)
        # 4) 几种方式都未找到Edge浏览器文件路径，抛出异常
        raise FileExistsError("未找到Edge浏览器")
