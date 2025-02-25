import json
import re
import tempfile
import time
import typing
from pathlib import Path

from PIL import Image
from selenium import common

from ..control_browser.control_browser import ControlBrowser
from ..entity.selenium_config import SeleniumConfig


class ControlDriver:

    @staticmethod
    def execute_js(selenium_config: SeleniumConfig, js: str):
        """执行js代码"""
        driver = ControlBrowser.get_driver(selenium_config)
        driver.execute_script(js)
        time.sleep(0.1)  # 执行结束之后等待一会

    @staticmethod
    def get_networks(selenium_config: SeleniumConfig) -> typing.List[dict]:
        """获取selenium运行中的network请求"""
        time.sleep(1)  # 等待页面请求发送
        driver = ControlBrowser.get_driver(selenium_config)
        # 1) 获取selenium的所有监听日志
        performance_log = driver.get_log("performance")
        # 2) 对日志进行处理并筛选
        # types = ['application/json']
        # filter_type = lambda _type: _type in types
        results = []
        for packet in performance_log:
            # noinspection PyBroadException
            try:
                # 2.1) 过滤掉10秒之前的日志
                if int(time.time() * 1000) - packet['timestamp'] >= 10 * 1000:
                    continue
                # 2.2) 获取message的数据
                message = json.loads(packet['message'])['message']
                # 2.3) 过滤所有非Network.responseReceived相关的日志
                if not re.match("Network", message['method']):
                    continue
                # 2.4) 获取请求参数
                params = message['params']
                request_id = params['requestId']  # 唯一的请求标识符（相当于该请求的身份证）
                url = params['response'].get('url')  # 该请求的url
                # # 2.5) 过滤获取该请求返回的type
                # if not filter_type(_type=params['response'].get('mimeType')):
                #     continue
                # 2.6) selenium调用cdp获取请求结果
                response = driver.execute_cdp_cmd("Network.getResponseBody", {'requestId': request_id})
                results.append({'timestamp': packet['timestamp'], 'url': url, 'response': response})
            except Exception:
                pass
        return results

    @staticmethod
    def open_url(selenium_config: SeleniumConfig, url: str):
        """打开url"""
        for _ in range(3):
            try:
                ControlBrowser.get_driver(selenium_config).get(url)
                break
            except OSError:  # selenium驱动升级会导致driver失效，会报错OSError
                selenium_config.info("selenium启动异常，重新启动")
                time.sleep(1)

    @staticmethod
    def refresh(selenium_config: SeleniumConfig):
        """刷新"""
        ControlBrowser.get_driver(selenium_config).refresh()

    @staticmethod
    def screenshot(selenium_config: SeleniumConfig, save_path: typing.Union[Path, str]) -> str:
        """截图"""
        # 1) 使用selenium方法进行截图
        save_path = tempfile.mktemp(".png") if save_path is None else str(save_path)
        try:
            ControlBrowser.get_driver(selenium_config).save_screenshot(save_path)
        except common.exceptions.NoSuchWindowException:
            raise RuntimeError("窗口已关闭，无法截图")
        # 2) 如果传入了元素，则截取元素所在位置
        # 注: 当浏览器滑动了之后，截图还是当前位置截图，但是计算元素坐标时，坐标并未变换，会导致裁剪出现的图片会有问题
        if selenium_config.element:
            try:
                # 2.1) 获取元素坐标信息
                left = int(selenium_config.element.rect['x'])
                right = left + int(selenium_config.element.rect['width'])
                top = int(selenium_config.element.rect['y'])
                bottom = top + int(selenium_config.element.rect['height'])
                # 2.2) 使用PIL读取图片并对其裁剪
                with Image.open(save_path) as image:
                    image = image.crop((left, top, right, bottom))
                    image.save(save_path)
            except Exception as e:
                selenium_config.error(f"图片裁剪失败: {e}")
        return save_path
