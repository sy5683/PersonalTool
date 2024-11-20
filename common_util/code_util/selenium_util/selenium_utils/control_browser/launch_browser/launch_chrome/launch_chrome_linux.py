import logging
import os
from pathlib import Path

import psutil

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
                if "chrome" in proc.info.get("name", "").lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                logging.warning(f"进程关闭失败: {name}")

    @classmethod
    def _get_chrome_path(cls) -> str:
        """获取谷歌浏览器路径"""
        # Linux只有一个根目录，因此直接获取这个根目录之后从中遍历全部文件路径
        for chrome_path in Path(os.path.abspath(os.sep)).rglob("google-chrome"):
            return str(chrome_path)
        raise FileExistsError("未找到谷歌浏览器路径")
