import abc

import flask

from .log_base import LogBase


class ServiceBase(LogBase, metaclass=abc.ABCMeta):

    def __init__(self, app: flask.Flask):
        super().__init__()
        self.app = app  # app服务

    @abc.abstractmethod
    def set_route(self, *args, **kwargs):
        """设置接口服务"""

    def run(self, port: int = 8080):
        """服务器启动方法"""
        # 1) 设置接口服务
        self.set_route()
        # 2) 运行服务接口
        self.app.run(host="0.0.0.0", port=port, threaded=True)
