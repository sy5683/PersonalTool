import os
from pathlib import Path

import psutil
from selenium import webdriver

from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from .launch_chrome import LaunchChrome


class LaunchChromeLinux(LaunchChrome):

    @classmethod
    def _close_browser_by_cmd(cls, selenium_config: SeleniumConfig):
        """命令行关闭浏览器"""
        # 使用psutil直接关闭chrome相关的进程
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            name = proc.info.get("name", "")
            try:
                if "chrome" in name.lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                selenium_config.error(f"进程关闭失败: {name}")

    @classmethod
    def _get_chrome_path(cls) -> str:
        """获取谷歌浏览器路径"""
        # Linux只有一个根目录，因此直接获取这个根目录之后从中遍历全部文件路径
        for chrome_path in Path(os.path.abspath(os.sep)).rglob("*google.chrome*"):
            if chrome_path.is_file():
                continue
            chrome_file_path = chrome_path.joinpath("files", "google", "chrome", "chrome")
            if chrome_file_path.exists():
                return str(chrome_file_path)
        raise FileExistsError("未找到谷歌浏览器路径")

    @classmethod
    def _set_special_options(cls, options: webdriver.ChromeOptions):
        """进行一些特殊设置"""
        options.binary_location = cls._get_chrome_path()
