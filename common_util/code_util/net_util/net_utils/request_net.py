import json
import logging
import tempfile
import time
import traceback

import requests


class RequestNet:

    @classmethod
    def download(cls, download_url: str, download_path: str, suffix: str, **kwargs) -> str:
        """下载文件"""
        # 1) get请求接口获取文件数据
        response = cls.request("GET", download_url, **kwargs)
        # 2) 将数据流写入下载文件路径
        download_path = tempfile.mktemp(".%s" % suffix.strip(".")) if download_path is None else str(download_path)
        with open(download_path, "wb") as file:
            file.write(response.content)
        time.sleep(1)  # 下载完成后必须强制等待一会，否则下载的文件会因为正在使用而导致无法复制、移动等处理
        return download_path

    @staticmethod
    def request(method: str, url: str, **kwargs) -> requests.Response:
        """发送请求"""
        # 1.1) 接口请求头封装一个默认的常用伪装，如果不需要这个请求头，传入一个None或者{}均可
        if "headers" not in kwargs:
            kwargs['headers'] = {'Content-Type': "application/json"}
        # 1.2) https请求需要关闭验证
        if url.startswith("https"):
            kwargs['verify'] = False
        # 2) request请求接口
        logging.info(f"请求: {url}\n请求参数: {kwargs}")
        try:
            with requests.request(method, url, **kwargs) as response:
                return response
        except Exception:
            raise Exception(f"请求失败: {url}\n{traceback.format_exc()}")

    @staticmethod
    def response_to_result(response: requests.Response, *keys) -> dict:
        """将requests请求返回的response转为可以阅读的结构化字典result"""
        # 1) json格式化解析接口返回的结果
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            raise ValueError(f"接口调用返回数据不为格式化字典数据: {response.text}")
        # 2) 根据每层的键，往里取出我们需要的值。如: {'key_1': {'key_2': "结果"}}
        for key in keys:
            try:
                result = result[key]
            except (KeyError, TypeError):
                raise KeyError(f"接口数据异常，无法定位指定键【{key}】: {result}")
        return result
