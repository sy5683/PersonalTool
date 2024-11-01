import typing

import flask
from flask import typing as ft, Response
from werkzeug.datastructures import MultiDict, ImmutableMultiDict


from .entity.flask_response import FlaskResponse


class FlaskUtil:

    @staticmethod
    def get_app(name: str) -> flask.app:
        """获取app服务"""

        class _Flask(flask.Flask):
            """使用视图重写Flask类，使接口返回统一值"""

            # 重写make_response方法
            def make_response(self, rv: ft.ResponseReturnValue) -> Response:
                if not isinstance(rv, FlaskResponse):
                    rv = FlaskResponse(data=rv)
                if isinstance(rv, FlaskResponse):
                    rv = rv.to_dict()
                return super().make_response(rv)

        app = _Flask(name)

        # 添加异常捕获，捕获所有异常，并返回统一的错误格式
        @app.errorhandler(Exception)
        def handle_exception(e):
            return FlaskResponse(code=-1, message=str(e))

        return app

    @classmethod
    def get_kwarg(cls, key: str) -> typing.Any:
        """获取参数"""
        return cls._get_kwargs().get(key)

    @staticmethod
    def run(app: flask.app, port: int = 8080):
        """运行接口"""
        app.run(host="0.0.0.0", port=port, threaded=True)

    @staticmethod
    def _get_kwargs() -> MultiDict[str, str] | ImmutableMultiDict[str, str]:
        """获取参数"""
        return flask.request.args if flask.request.method == "GET" else flask.request.form
