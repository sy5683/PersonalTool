import os
import subprocess
from pathlib import Path

from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from .launch_chrome import LaunchChrome


class LaunchChromeLinux(LaunchChrome):

    @classmethod
    def _close_browser_by_cmd(cls, selenium_config: SeleniumConfig):
        """命令行关闭浏览器"""
        # TODO 需要具体实现
        # 1) 使用命令行直接关闭进程
        # 2) 如果控制debug接管的浏览器，使用driver.quit()仅会关闭selenium，因此需要将端口也进行处理

    @classmethod
    def _get_chrome_path(cls) -> str:
        """获取谷歌浏览器路径"""
        # Linux只有一个根目录，因此直接获取这个根目录之后从中遍历全部文件路径
        for chrome_path in Path(os.path.abspath(os.sep)).rglob("google-chrome"):
            return str(chrome_path)
        raise FileExistsError("未找到谷歌浏览器路径")
