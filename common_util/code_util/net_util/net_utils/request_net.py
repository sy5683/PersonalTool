import json
import logging
import re
import tempfile
from json import JSONDecodeError

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
    def response_to_result(response: requests.Response, *keys) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        try:
            result = json.loads(response.text)
        except JSONDecodeError:
            raise ValueError(f"接口调用返回数据不为格式化字典数据: {response.text}")
        for key in keys:
            try:
                result = result[key]
            except (KeyError, TypeError):
                raise KeyError(f"接口数据异常，无法定位指定键【{key}】: {result}")
        return result
