import logging
import os
import re
import subprocess
import sys
import threading
import time
import traceback
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver
from selenium.common import InvalidArgumentException, SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from .download_driver import DownloadDriver
from .launch_base import LaunchBase
from ..selenium_config import SeleniumConfig


class LaunchChrome(LaunchBase):
    __driver_map: typing.Dict[int, WebDriver] = {}
    __debug_driver_map: typing.Dict[int, WebDriver] = {}

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        debug_port = cls.__format_debug_port(**kwargs)
        if debug_port is None:
            # 获取进程id，并启动谷歌浏览器
            thread_id = threading.current_thread().ident
            if thread_id not in cls.__driver_map:
                cls.__driver_map[thread_id] = cls._launch_chrome(**kwargs)
            return cls.__driver_map[thread_id]
        else:
            # 使用debug方式接管谷歌浏览器
            if debug_port not in cls.__debug_driver_map:
                cls.__debug_driver_map[debug_port] = cls._take_over_chrome(debug_port)
            return cls.__debug_driver_map[debug_port]

    @classmethod
    def launch_browser_debug(cls, debug_port: int):
        """debug启动谷歌浏览器"""
        debug_port = cls.__format_debug_port(debug_port=debug_port)
        if debug_port in cls.__driver_map:
            logging.info(f"Debug端口的谷歌浏览器正在运行: {debug_port}")
            return
        assert debug_port, "端口号不可为0"
        assert not cls._netstat_debug_port_running(debug_port), f"Debug端口被占用: {debug_port}"
        logging.info(f"Debug启动谷歌浏览器: {debug_port}")
        # 1) 获取谷歌浏览器路径
        chrome_path = cls._get_chrome_path()
        # 2) cmd调用命令行debug启动谷歌浏览器
        subprocess.Popen(f'"{chrome_path}" "--remote-debugging-port={debug_port}"')
        # 3) 需要等待一秒，确认端口正常启动
        time.sleep(1)

    @classmethod
    def close_browser(cls, **kwargs):
        """关闭谷歌浏览器"""
        driver = kwargs.get("driver", cls.get_driver(**kwargs))
        if driver is not None:
            # 1) 使用selenium自带的quit方法关闭driver
            driver.quit()
            time.sleep(1)
            # 2) 因为经常出现quit之后cmd窗口未关的情况，因此这里使用命令行直接关闭进程
            os.system(f"taskkill /f /im {os.path.basename(DownloadDriver.get_chrome_driver_path())}")
            # 3) 如果控制debug接管的浏览器，使用driver.quit()仅会关闭selenium，因此需要将端口也进行处理
            debug_port = cls.__format_debug_port(**kwargs)
            if debug_port and cls._netstat_debug_port_running(debug_port):
                with os.popen(f'netstat -aon|findstr "{debug_port}"') as cmd:
                    result = cmd.read()
                temp_result = [each for each in result.split('\n')[0].split(' ') if each != '']
                os.system(f"taskkill /f /pid {temp_result[4]}")
            for thread_id, _driver in list(cls.__driver_map.items()):
                if driver == _driver:
                    del cls.__driver_map[thread_id]
            for _debug_port, _driver in list(cls.__debug_driver_map.items()):
                if driver == _driver:
                    del cls.__debug_driver_map[_debug_port]

    @classmethod
    def _launch_chrome(cls, **kwargs) -> WebDriver:
        """启动谷歌浏览器"""
        logging.info("启动谷歌浏览器")
        try:
            assert kwargs.get("use_user_data", True)
            # 1.1) 获取谷歌浏览器用户缓存路径
            user_data_dir = cls._get_chrome_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_chrome_driver(user_data_dir)
        except (AssertionError, InvalidArgumentException, SessionNotCreatedException):
            # 2) 重新获取driver，不加载user_data_dir
            driver = cls._get_chrome_driver()
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(SeleniumConfig.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    def _take_over_chrome(cls, debug_port: int) -> WebDriver:
        """接管谷歌浏览器"""
        assert cls._netstat_debug_port_running(debug_port), f"当前端口并未启动，无法接管谷歌浏览器: {debug_port}"
        logging.info(f"接管已debug运行的谷歌浏览器，端口: {debug_port}")
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
        # 1.2) 添加debug地址
        options.debugger_address = f"127.0.0.1:{debug_port}"  # 地址为本地，只需要指定端口
        # 2) 接管谷歌浏览器
        driver = cls.__launch_chrome_driver(options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(SeleniumConfig.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        # 4) 接管切换浏览器页签至最后一个
        driver.switch_to.window(driver.window_handles[-1])
        return driver

    @classmethod
    def _get_chrome_driver(cls, user_data_dir: str = None) -> WebDriver:
        """获取chrome_driver"""
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
        # 1.2.1) 设置静默运行
        if SeleniumConfig.headless:
            options.add_argument('--headless')
        # 1.2.2) 设置ip代理
        if SeleniumConfig.proxy_ip:
            options.add_argument(f"--proxy-server={SeleniumConfig.proxy_ip}")
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
        # 取消提示和默认下载路径在同一个参数中配置
        prefs = options.experimental_options.get("prefs", {})
        # 1.5) 设置取消提示
        prefs.update({'credentials_enable_service': False})  # 设置取消提示保存密码
        prefs.update({'download.prompt_for_download': False})  # 取消提示下载
        # 1.6) 设置默认下载路径
        logging.info(f"浏览器下载路径为: {SeleniumConfig.download_path}")
        if os.path.exists(SeleniumConfig.download_path):
            prefs.update({'download.default_directory': SeleniumConfig.download_path})
        options.add_experimental_option('prefs', prefs)
        # 1.7) 设置读取用户缓存目录
        if user_data_dir and os.path.exists(user_data_dir):
            options.add_argument(f"--user-data-dir={user_data_dir}")
        # 2) 启动谷歌浏览器
        return cls.__launch_chrome_driver(options)

    @staticmethod
    def _get_chrome_path() -> str:
        """获取谷歌浏览器路径"""
        # 1) 通过注册表查找谷歌浏览器路径
        for regedit_dir in [win32con.HKEY_LOCAL_MACHINE, win32con.HKEY_CURRENT_USER]:  # 谷歌浏览器路径注册表一般在这两个位置下固定位置
            regedit_path = "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe"
            try:
                key = win32api.RegOpenKey(regedit_dir, regedit_path)
                chrome_path, _ = win32api.RegQueryValueEx(key, "path")
            except pywintypes.error:
                continue
            chrome_path = os.path.join(chrome_path, "chrome.exe")
            if os.path.isfile(chrome_path):
                return chrome_path
        # 2) 通过遍历谷歌浏览器常用安装路径查找谷歌浏览器路径
        for chrome_parent_path in [os.path.join(os.path.expanduser('~'), "AppData\\Local"), "C:\\Program Files",
                                   "C:\\Program Files (x86)"]:
            chrome_path = os.path.join(chrome_parent_path, "Google\\Chrome\\Application\\chrome.exe")
            if os.path.isfile(chrome_path):
                return chrome_path
        # 3) 某些极个别特殊情况，用户直接解压绿色文件使用谷歌浏览器，这时候注册表没值路径也不确定，因此只能遍历全部文件路径
        for root_path in re.findall(r"(.:\\)", win32api.GetLogicalDriveStrings()):
            # 使用pathlib的rglob遍历，比for循环遍历更快，代码更简单
            for chrome_path in Path(root_path).rglob("chrome.exe"):
                return str(chrome_path)
        raise FileExistsError("未找到谷歌浏览器路径")

    @classmethod
    def _get_chrome_user_data_path(cls) -> typing.Union[str, None]:
        """获取谷歌浏览器用户缓存User Data路径"""
        # 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Google\\Chrome\\User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        # 有的User Data文件放在谷歌浏览器同级目录中
        user_data_path = os.path.join(os.path.dirname(cls._get_chrome_path()), "User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        return None

    @staticmethod
    def _netstat_debug_port_running(debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        # noinspection PyBroadException
        try:
            if sys.platform == "win32":
                cmd = f'netstat -ano | findstr "{debug_port}" | findstr "LISTEN"'
            else:
                cmd = f'netstat -ano | grep {debug_port} | grep LISTEN'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(debug_port) in p.stdout.read()
        except Exception:
            logging.error(traceback.format_exc())
            return False

    @classmethod
    def __format_debug_port(cls, **kwargs) -> int:
        debug_port = kwargs.get("debug_port")
        if debug_port is None:
            # 未启动driver并且默认debug端口正在运行
            if not cls.__driver_map and cls._netstat_debug_port_running(SeleniumConfig.default_debug_port):
                return SeleniumConfig.default_debug_port
        return debug_port

    @staticmethod
    def __launch_chrome_driver(options: webdriver.ChromeOptions) -> WebDriver:
        """启动谷歌浏览器driver"""
        driver_path = DownloadDriver.get_chrome_driver_path()
        service = Service(executable_path=driver_path)
        return webdriver.Chrome(options=options, service=service)
