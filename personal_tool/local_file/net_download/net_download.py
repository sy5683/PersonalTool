import os.path
import os.path
import subprocess
from pathlib import Path
from typing import Tuple, Union

from base.tool_base import ToolBase


class NetDownload(ToolBase):
    """下载工具"""

    def __init__(self, download_path: Union[str, Path, None] = None):
        self.download_path = download_path if download_path is None else str(download_path)

    def main(self, function=None, url: str = None):
        if function and url:
            function(url)

    def bilibili_download(self, url: str):
        """下载哔哩哔哩"""
        self._cd_to_download_path()
        self._cmd_popen(f"you-get {url}")

    def _cd_to_download_path(self):
        """cd命令跳转至指定下载路径"""
        if self.download_path is not None:
            self._cmd_popen(os.path.abspath(self.download_path)[:2])  # 跳转至根目录
            self._cmd_popen(f"cd {self.download_path}")  # 跳转至指定目录

    @staticmethod
    def _cmd_popen(cmd: str) -> Tuple[str, str]:
        """popen运行cmd命令"""
        return subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='gbk').communicate()


if __name__ == '__main__':
    net_download = NetDownload("E:\\Download")
    net_download.main(NetDownload.bilibili_download, url="")
