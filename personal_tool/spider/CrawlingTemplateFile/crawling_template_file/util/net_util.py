import json
import logging
from pathlib import Path

import requests
from requests import Response

from .file_util import FileUtil


class NetUtil:

    @classmethod
    def download(cls, download_url: str, suffix: str = 'tmp') -> Path:
        """下载文件"""
        download_path = FileUtil.get_temp_file_path(suffix)
        response = cls.request("get", download_url)
        with open(str(download_path), "wb") as file:
            file.write(response.content)
        return download_path

    @classmethod
    def request(cls, method: str, url: str, wait_seconds: int = 120, **kwargs) -> Response:
        """发送请求"""
        kwargs['timeout'] = kwargs.get('timeout', (wait_seconds, wait_seconds * 3))  # 两个时间分别是：请求超时时间，响应超时时间
        return requests.request(method, url, **kwargs)

    @staticmethod
    def response_to_result(response: Response) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        try:
            return json.loads(response.text)
        except Exception:
            logging.error(f"接口调用返回数据不为格式化字典数据: {response.text}")
            raise Exception(f"接口调用失败 {response.status_code}")
