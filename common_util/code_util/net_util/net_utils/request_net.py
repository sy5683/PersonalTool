import json
import logging
import re
import tempfile

import requests


class RequestNet:

    @classmethod
    def download(cls, download_url: str, download_path: str, suffix: str, **kwargs) -> str:
        """下载文件"""
        response = cls.request("GET", download_url, **kwargs)
        download_path = str(download_path) or tempfile.mktemp(".%s" % re.sub(r"^\.+", "", suffix))
        with open(download_path, "wb") as file:
            file.write(response.content)
        return download_path

    @staticmethod
    def request(method: str, url: str, **kwargs) -> requests.Response:
        """发送请求"""
        if kwargs.get("headers") is None:
            kwargs['headers'] = {'Content-Type': "application/json"}
        if url.startswith("https"):
            kwargs['verify'] = False  # https 请求需要关闭验证
        logging.info(f"请求: {url} \n请求参数: {kwargs}")
        with requests.request(method, url, **kwargs) as response:
            return response

    @staticmethod
    def response_to_result(response: requests.Response) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        return json.loads(response.text)
