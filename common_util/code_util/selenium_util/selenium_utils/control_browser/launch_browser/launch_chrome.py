import logging
import os
import re
import subprocess
import threading
import time
import traceback
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver, common
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from .base.launch_base import LaunchBase
from .download_driver import DownloadDriver
from ...entity.selenium_config import SeleniumConfig


class LaunchChrome(LaunchBase):
    _driver_map: typing.Dict[int, WebDriver] = {}

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        driver = selenium_config.driver
        if driver is None:
            debug_port = cls.__get_debug_port(selenium_config)
            driver = cls._driver_map.get(debug_port if debug_port else threading.current_thread().ident)
        if driver is None:
            return
        # 2) 使用selenium自带的quit方法关闭driver
        driver.quit()
        time.sleep(1)
        # 3) 因为经常出现quit之后cmd窗口未关的情况，因此这里使用命令行直接关闭进程
        if selenium_config.close_task:
            os.system(f"taskkill /f /im {os.path.basename(cls.__get_driver_path(selenium_config))}")
        # 4) 如果控制debug接管的浏览器，使用driver.quit()仅会关闭selenium，因此需要将端口也进行处理
        debug_port = cls.__get_debug_port(selenium_config)
        if debug_port and cls.__netstat_debug_port_running(debug_port):
            with os.popen(f'netstat -aon|findstr "{debug_port}"') as cmd:
                result = cmd.read()
            temp_result = [each for each in result.split('\n')[0].split(' ') if each != '']
            os.system(f"taskkill /f /pid {temp_result[4]}")
        # 5) 清除缓存
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
        # 2) 获取debug端口
        debug_port = cls.__get_debug_port(selenium_config)
        # 3.1) 获取进程id，并启动谷歌浏览器
        if debug_port is None:
            thread_id = threading.current_thread().ident
            if thread_id not in cls._driver_map:
                cls._driver_map[thread_id] = cls._launch_chrome(selenium_config)
            return cls._driver_map[thread_id]
        # 3.2) 使用debug方式接管谷歌浏览器
        else:
            if debug_port not in cls._driver_map:
                cls._driver_map[debug_port] = cls._take_over_chrome(selenium_config)
            return cls._driver_map[debug_port]

    @classmethod
    def launch_browser_debug(cls, selenium_config: SeleniumConfig):
        """debug启动谷歌浏览器"""
        # 1) 检测debug端口
        debug_port = cls.__get_debug_port(selenium_config, True)
        if debug_port and debug_port in cls._driver_map:
            logging.info(f"Debug端口的谷歌浏览器正在运行: {debug_port}")
            return
        assert debug_port > 0, f"端口号异常: {debug_port}"
        assert not cls.__netstat_debug_port_running(debug_port), f"Debug端口被占用: {debug_port}"
        selenium_config.info(f"Debug启动谷歌浏览器: {debug_port}")
        # 2) 获取谷歌浏览器路径
        chrome_path = cls._get_chrome_path()
        # 3) cmd调用命令行debug启动谷歌浏览器
        subprocess.Popen(f'"{chrome_path}" "--remote-debugging-port={debug_port}"')
        time.sleep(1)  # 等待一秒，确认端口正常启动

    @classmethod
    def _get_chrome_driver(cls, selenium_config: SeleniumConfig, user_data_dir: str = None) -> WebDriver:
        """获取chrome_driver"""
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
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
        # 2) 启动谷歌浏览器
        return cls.__launch_chrome_driver(selenium_config, options)

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
            for chrome_path in Path(root_path).rglob("chrome.exe"):
                return str(chrome_path)
        raise FileExistsError("未找到谷歌浏览器路径")

    @classmethod
    def _launch_chrome(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动谷歌浏览器"""
        logging.info("启动谷歌浏览器")
        try:
            assert selenium_config.use_user_data
            # 1.1) 获取谷歌浏览器用户缓存路径
            user_data_dir = cls.__get_chrome_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_chrome_driver(selenium_config, user_data_dir)
        except (AssertionError, common.InvalidArgumentException, common.SessionNotCreatedException):
            # 2) 重新获取driver，不加载user_data_dir
            driver = cls._get_chrome_driver(selenium_config)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    def _take_over_chrome(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """接管谷歌浏览器"""
        debug_port = cls.__get_debug_port(selenium_config)
        assert cls.__netstat_debug_port_running(debug_port), f"当前端口并未启动，无法接管谷歌浏览器: {debug_port}"
        logging.info(f"接管已debug运行的谷歌浏览器，端口: {debug_port}")
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
        # 1.2) 添加debug地址
        options.debugger_address = f"127.0.0.1:{debug_port}"  # 地址为本地，只需要指定端口
        # 2) 接管谷歌浏览器
        driver = cls.__launch_chrome_driver(selenium_config, options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        # 4) 接管切换浏览器页签至最后一个
        driver.switch_to.window(driver.window_handles[-1])
        return driver

    @classmethod
    def __get_debug_port(cls, selenium_config: SeleniumConfig, return_default: bool = False) -> typing.Union[int, None]:
        """获取debug端口"""
        # 1) 获取参数中的debug_port
        if selenium_config.debug_port:
            return selenium_config.debug_port
        # 2) 返回默认的debug_port
        default_debug_port = 9222
        # 如果需要返回默认的debug_port，则无需进行判断debug_port是否正在运行，直接返回
        if return_default:
            return default_debug_port
        # 检测默认的debug_port是否正在运行，如果正在运行，则返回默认的debug_port
        if cls.__netstat_debug_port_running(default_debug_port):
            return default_debug_port
        # 3) 返回空值
        return None

    @classmethod
    def __get_chrome_user_data_path(cls) -> typing.Union[str, None]:
        """获取谷歌浏览器用户缓存User Data路径"""
        # 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Google\\Chrome\\User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        # 有的User Data文件放在谷歌浏览器同级目录中
        user_data_path = os.path.join(os.path.dirname(cls._get_chrome_path()), "User Data\\Default")
        if os.path.exists(user_data_path):
            return user_data_path
        # 返回空值
        return None

    @staticmethod
    def __get_driver_path(selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 使用参数中的driver_path
        if selenium_config.driver_path:
            return selenium_config.driver_path
        # 自动获取下载的driver_path路径
        return DownloadDriver.get_chrome_driver_path()

    @classmethod
    def __launch_chrome_driver(cls, selenium_config: SeleniumConfig, options: webdriver.ChromeOptions) -> WebDriver:
        """启动谷歌浏览器driver"""
        driver_path = cls.__get_driver_path(selenium_config)
        service = Service(executable_path=driver_path)
        return webdriver.Chrome(options=options, service=service)

    @staticmethod
    def __netstat_debug_port_running(debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        try:
            cmd = f'netstat -ano | findstr "{debug_port}" | findstr "LISTEN"'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(debug_port) in p.stdout.read()
        except Exception as e:
            logging.warning(f"{e}\n{traceback.format_exc()}")
            return False
