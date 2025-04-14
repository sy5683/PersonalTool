import typing
from pathlib import Path

import requests

from .net_utils.request_net import RequestNet


class NetUtil:

    @staticmethod
    def download(download_url: str, download_path: typing.Union[Path, str] = None, suffix: str = 'tmp', **kwargs) -> str:
        """下载文件"""
        return RequestNet.download(download_url, download_path, suffix, **kwargs)

    @staticmethod
    def request(method: str, url: str, **kwargs) -> requests.Response:
        """发送请求"""
        return RequestNet.request(method, url, **kwargs)

    @staticmethod
    def response_to_result(response: requests.Response, *keys: str) -> typing.Union[dict, list]:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        return RequestNet.response_to_result(response, *keys)
