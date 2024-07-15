import json
import logging
import re
import tempfile

import requests


class RequestNet:

    @staticmethod
    def download(download_url: str, download_path: str, suffix: str, **kwargs) -> str:
        """下载文件"""
        logging.info(f"下载文件: {download_url}")
        response = requests.request("GET", download_url, **kwargs)
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
        logging.info(f"请求: {url} \n 请求参数: {kwargs}")
        return requests.request(method, url, **kwargs)

    @staticmethod
    def response_to_result(response: requests.Response) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        return json.loads(response.text)
