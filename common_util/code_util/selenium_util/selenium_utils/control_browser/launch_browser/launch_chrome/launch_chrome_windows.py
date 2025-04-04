import os
import re
import subprocess
from pathlib import Path

import win32con
from selenium import webdriver
from win32api import GetLogicalDriveStrings, RegOpenKey, RegQueryValueEx

from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from .launch_chrome import LaunchChrome


class LaunchChromeWindows(LaunchChrome):

    @classmethod
    def _close_browser_by_cmd(cls, selenium_config: SeleniumConfig):
        """命令行关闭浏览器"""
        # 1) 使用命令行直接关闭进程
        if selenium_config.close_task:
            os.system(f"taskkill /f /im {os.path.basename(cls._get_driver_path(selenium_config))}")
        # 2) 如果控制debug接管的浏览器，使用driver.quit()仅会关闭selenium，因此需要将端口也进行处理
        debug_port = cls._get_debug_port(selenium_config)
        if debug_port and cls._netstat_debug_port_running(debug_port):
            with os.popen(f'netstat -aon|findstr "{debug_port}"') as cmd:
                result = cmd.read()
            temp_result = [each for each in result.split('\n')[0].split(' ') if each != '']
            os.system(f"taskkill /f /pid {temp_result[4]}")

    @classmethod
    def _get_chrome_path(cls, selenium_config: SeleniumConfig) -> str:
        """获取谷歌浏览器路径"""
        # 1) 通过注册表查找谷歌浏览器路径
        for regedit_dir in [win32con.HKEY_LOCAL_MACHINE, win32con.HKEY_CURRENT_USER]:  # 谷歌浏览器路径注册表一般在这两个位置下固定位置
            regedit_path = os.path.join("Software", "Microsoft", "Windows", "CurrentVersion", "App Paths", "chrome.exe")
            try:
                key = RegOpenKey(regedit_dir, regedit_path)
                chrome_path, _ = RegQueryValueEx(key, "path")
            except (FileNotFoundError, PermissionError, WindowsError, ValueError, TypeError):
                continue
            chrome_path = os.path.join(chrome_path, "chrome.exe")
            if os.path.isfile(chrome_path):
                return chrome_path
        # 2) 通过遍历谷歌浏览器常用安装路径查找谷歌浏览器路径
        for chrome_parent_path in [os.path.join(os.path.expanduser('~'), "AppData", "Local"),
                                   os.path.join("C:/", "Program Files"),
                                   os.path.join("C:/", "Program Files (x86)")]:
            chrome_path = os.path.join(chrome_parent_path, "Google", "Chrome", "Application", "chrome.exe")
            if os.path.isfile(chrome_path):
                return chrome_path
        # 3) 某些极个别特殊情况，用户直接解压绿色文件使用谷歌浏览器，这时候注册表没值路径也不确定，因此只能遍历全部文件路径
        for root_path in re.findall(r"(.:/)", GetLogicalDriveStrings()):
            for chrome_path in Path(root_path).rglob("chrome.exe"):
                return str(chrome_path)
        # 4) 几种方式都未找到谷歌浏览器文件路径，抛出异常
        raise FileExistsError("未找到谷歌浏览器")

    @classmethod
    def _netstat_debug_port_running(cls, debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        # noinspection PyBroadException
        try:
            cmd = f'netstat -ano | findstr "{debug_port}" | findstr "LISTEN"'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(debug_port) in p.stdout.read()
        except Exception:
            return False

    @classmethod
    def _set_special_options(cls, options: webdriver.ChromeOptions):
        """进行一些特殊设置"""
