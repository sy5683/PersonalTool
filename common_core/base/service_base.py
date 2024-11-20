import abc

import flask

from .log_base import LogBase


class ServiceBase(LogBase, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()
        # 获取app服务
        self.app = flask.Flask(self.get_subclass_path().parent.name)

        # 添加异常捕获，捕获所有异常，并返回统一的错误格式
        @self.app.errorhandler(Exception)
        def handle_exception(e) -> dict:
            return {'code': -1, 'message': str(e)}

    @abc.abstractmethod
    def set_route(self, *args, **kwargs):
        """设置接口服务"""

    def run(self, port: int = 8080):
        """服务器启动方法"""
        # 1) 设置接口服务
        self.set_route()
        # 2) 运行服务接口
        self.app.run(host="0.0.0.0", port=port, threaded=True)
