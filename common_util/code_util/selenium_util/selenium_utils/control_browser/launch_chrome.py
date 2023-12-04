import logging
import os
import re
import subprocess
import sys
import traceback
import typing
from pathlib import Path

import pywintypes
import win32api
import win32con
from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from common_core.base.exception_base import FileFindError
from common_util.code_util.selenium_util.selenium_utils.control_browser.download_driver import DownloadDriver
from .launch_base import LaunchBase
from ..selenium_config import SeleniumConfig


class LaunchChrome(LaunchBase):
    __debug_port = 9222

    @classmethod
    def launch_browser(cls) -> WebDriver:
        """启动谷歌浏览器"""
        if cls.__netstat_debug_port_running():
            logging.info(f"接管已debug运行的谷歌浏览器，端口: {cls.__debug_port}")
            # 1.1.1) 获取谷歌浏览器设置
            options = webdriver.ChromeOptions()
            # 1.1.2) 添加debug地址
            options.debugger_address = f"127.0.0.1:{cls.__debug_port}"  # 地址为本地，只需要指定端口
            # 1.2) 接管谷歌浏览器
            driver = cls.__launch_chrome_driver(options)
            # 1.3) 接管切换浏览器页签至最后一个
            driver.switch_to.window(driver.window_handles[-1])
        else:
            logging.info("启动谷歌浏览器")
            try:
                # 2.1.1) 获取谷歌浏览器用户缓存路径
                user_data_dir = cls._get_chrome_user_data_path()
                # 2.1.2) 获取driver
                driver = cls._get_chrome_driver(user_data_dir=user_data_dir)
            except InvalidArgumentException:
                # 2.1.3) 重新获取driver，不加载user_data_dir
                driver = cls._get_chrome_driver()
        return driver

    @classmethod
    def launch_browser_debug(cls):
        """debug启动谷歌浏览器"""
        if cls.__netstat_debug_port_running():
            logging.info(f"Debug端口正在运行: {cls.__debug_port}")
            return
        logging.info("debug启动谷歌浏览器")
        # 1) 获取谷歌浏览器路径
        chrome_path = cls._get_chrome_path()
        # 2) cmd调用命令行debug启动谷歌浏览器
        cmd = f'"{chrome_path}" "--remote-debugging-port={cls.__debug_port}"'
        subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='gbk').communicate()

    @classmethod
    def close_browser(cls, driver: WebDriver):
        """关闭谷歌浏览器"""
        # 1) 使用selenium自带的quit方法关闭driver
        driver.quit()
        # 2) 因为经常出现quit之后cmd窗口未关的情况，因此这里使用命令行直接关闭进程
        driver_path = DownloadDriver.get_chrome_driver_path()
        driver_name = os.path.basename(driver_path)
        os.system(f"taskkill /f /im {driver_name}")
        # 2) 如果控制debug接管的浏览器，使用driver.quit()仅会关闭selenium，因此需要将端口也进行处理
        if cls.__netstat_debug_port_running():
            with os.popen(f'netstat -aon|findstr "{cls.__debug_port}"') as cmd:
                result = cmd.read()
            temp_result = [each for each in result.split('\n')[0].split(' ') if each != '']
            os.system(f"taskkill /f /pid {temp_result[4]}")

    @classmethod
    def _get_chrome_driver(cls, user_data_dir: str = None) -> WebDriver:
        """获取chrome_driver"""
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
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
        raise FileFindError("未找到谷歌浏览器路径")

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
    def __launch_chrome_driver(options: webdriver.ChromeOptions) -> WebDriver:
        """启动谷歌浏览器"""
        driver_path = DownloadDriver.get_chrome_driver_path()
        service = Service(executable_path=driver_path)
        return webdriver.Chrome(options=options, service=service)

    @classmethod
    def __netstat_debug_port_running(cls) -> bool:
        """判断debug端口是否正在运行"""
        # noinspection PyBroadException
        try:
            if sys.platform == "win32":
                cmd = f'netstat -ano | findstr "{cls.__debug_port}" | findstr "LISTEN"'
            else:
                cmd = f'netstat -ano | grep {cls.__debug_port} | grep LISTEN'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(cls.__debug_port) in p.stdout.read()
        except Exception:
            logging.error(traceback.format_exc())
            return False
