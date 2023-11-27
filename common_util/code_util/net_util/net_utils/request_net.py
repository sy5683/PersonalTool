import json
import re
import tempfile

import requests


class RequestNet:

    @staticmethod
    def download(download_url: str, download_path: str, suffix: str, **kwargs) -> str:
        """下载文件"""
        response = requests.request("GET", download_url, **kwargs)
        download_path = str(download_path) or f"{tempfile.mktemp()}.%s" % re.sub(r"^\.+", "", suffix)
        with open(download_path, "wb") as file:
            file.write(response.content)
        return download_path

    @staticmethod
    def request(method: str, url: str, **kwargs) -> requests.Response:
        """发送请求"""
        return requests.request(method, url, **kwargs)

    @staticmethod
    def response_to_result(response: requests.Response) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        return json.loads(response.text)
