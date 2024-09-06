import logging
import os
import re
import threading
import time
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver, common
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver

from .base.launch_base import LaunchBase
from .download_driver import DownloadDriver
from ...entity.selenium_config import SeleniumConfig


class LaunchEdge(LaunchBase):
    _driver_map: typing.Dict[int, WebDriver] = {}

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭Edge浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        driver = selenium_config.driver
        if driver is None:
            driver = cls._driver_map.get(threading.current_thread().ident)
        if driver is None:
            return
        # 2) 使用selenium自带的quit方法关闭driver
        driver.quit()
        time.sleep(1)
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
        # 2) 获取进程id，并启动Edge浏览器
        thread_id = threading.current_thread().ident
        if thread_id not in cls._driver_map:
            cls._driver_map[thread_id] = cls._launch_edge(selenium_config)
        return cls._driver_map[thread_id]

    @classmethod
    def _get_edge_driver(cls, selenium_config: SeleniumConfig, user_data_dir: str = None) -> WebDriver:
        """获取edge_driver"""
        # 1.1) 获取Edge浏览器设置
        options = webdriver.EdgeOptions()
        # 1.2.1) 设置静默运行
        if selenium_config.headless:
            options.add_argument('--headless')
        # 1.2.2) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3.1) 设置忽略私密链接警告
        options.add_argument('--ignore-certificate-errors')
        # 1.3.2) 设置取消提示受自动控制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # 1.4.1) 伪装浏览器请求头
        options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        # 1.4.2) 去掉webdriver痕迹
        options.add_argument("disable-blink-features=AutomationControlled")
        # 1.5) 取消提示和默认下载路径在同一个参数中配置
        prefs = options.experimental_options.get("prefs", {})
        # 1.5.1) 设置取消提示
        prefs.update({'credentials_enable_service': False})  # 设置取消提示保存密码
        prefs.update({'download.prompt_for_download': False})  # 取消提示下载
        # 1.5.2) 设置默认下载路径
        logging.info(f"浏览器下载路径为: {selenium_config.download_path}")
        if os.path.exists(selenium_config.download_path):
            prefs.update({'download.default_directory': selenium_config.download_path})
        options.add_experimental_option('prefs', prefs)
        # 1.6) 设置读取用户缓存目录
        if user_data_dir and os.path.exists(user_data_dir):
            options.add_argument(f"--user-data-dir={user_data_dir}")
        # 2) 启动Edge浏览器
        return cls.__launch_edge_driver(selenium_config, options)

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

    @classmethod
    def _launch_edge(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动Edge浏览器"""
        logging.info("启动Edge浏览器")
        try:
            assert selenium_config.use_user_data
            # 1.1) 获取Edge浏览器用户缓存路径
            user_data_dir = cls.__get_edge_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_edge_driver(selenium_config, user_data_dir)
        except (AssertionError, common.InvalidArgumentException, common.SessionNotCreatedException):
            # 1.3) 重新获取driver，不加载user_data_dir
            driver = cls._get_edge_driver(selenium_config)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    def _launch_edge_with_ie(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """ie模式启动Edge浏览器"""
        logging.info("ie模式启动Edge浏览器")
        from .launch_ie import LaunchIe
        # 1.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 1.2.1) IE浏览器无法设置静默运行
        # 1.2.2) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3) 使用edge启动
        options.attach_to_edge_chrome = True
        options.edge_executable_path = cls._get_edge_path()
        # 2) 启动IE浏览器
        driver = LaunchIe._launch_ie_driver(selenium_config, options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver


    @staticmethod
    def __get_driver_path(selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 使用参数中的driver_path
        if selenium_config.driver_path:
            return selenium_config.driver_path
        # 自动获取下载的driver_path路径
        return DownloadDriver.get_edge_driver_path()

    @staticmethod
    def __get_edge_user_data_path() -> typing.Union[str, None]:
        """获取Edge浏览器用户缓存User Data路径"""
        # 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        # 返回空值
        return None

    @classmethod
    def __launch_edge_driver(cls, selenium_config: SeleniumConfig, options: webdriver.EdgeOptions) -> WebDriver:
        """启动Edge浏览器driver"""
        driver_path = cls.__get_driver_path(selenium_config)
        service = EdgeService(executable_path=driver_path)
        return webdriver.Edge(options=options, service=service)
