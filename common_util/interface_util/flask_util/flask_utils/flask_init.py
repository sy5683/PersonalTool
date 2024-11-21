import flask
from flask import typing as ft, Response

from .entity.flask_response import FlaskResponse


class _Flask(flask.Flask):
    """使用视图重写Flask类，使接口返回统一值"""

    # 重写make_response方法
    def make_response(self, rv: ft.ResponseReturnValue) -> Response:
        if not isinstance(rv, FlaskResponse):
            rv = FlaskResponse(data=rv)
        if isinstance(rv, FlaskResponse):
            rv = rv.to_dict()
        return super().make_response(rv)


class FlaskInit:

    @staticmethod
    def get_app(name: str) -> flask.app:
        """获取app服务"""
        app = _Flask(name)

        # 添加异常捕获，捕获所有异常，并返回统一的错误格式
        @app.errorhandler(Exception)
        def handle_exception(e) -> FlaskResponse:
            return FlaskResponse(code=-1, message=str(e))

        return app
