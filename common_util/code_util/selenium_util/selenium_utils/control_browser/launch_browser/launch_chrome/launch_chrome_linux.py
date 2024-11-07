import os
from pathlib import Path


from .launch_chrome import LaunchChrome


class LaunchChromeLinux(LaunchChrome):

    @classmethod
    def _get_chrome_path(cls) -> str:
        """获取谷歌浏览器路径"""
        # Linux只有一个根目录，因此直接获取这个根目录之后从中遍历全部文件路径
        for chrome_path in Path(os.path.abspath(os.sep)).rglob("chrome.exe"):
            return str(chrome_path)
        raise FileExistsError("未找到谷歌浏览器路径")
