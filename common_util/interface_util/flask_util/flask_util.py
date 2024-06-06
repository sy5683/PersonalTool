import flask
from werkzeug.datastructures import MultiDict, ImmutableMultiDict


class FlaskUtil:

    @staticmethod
    def get_app(name: str):
        """获取app服务"""
        return flask.Flask(name)

    @classmethod
    def get_kwarg(cls, key: str):
        """获取参数"""
        return cls._get_kwargs().get(key)

    @staticmethod
    def run(app: flask.app):
        """运行接口"""
        app.run(host="0.0.0.0", port=8080, threaded=True)

    @staticmethod
    def _get_kwargs() -> MultiDict[str, str] | ImmutableMultiDict[str, str]:
        """获取参数"""
        return flask.request.args if flask.request.method == "GET" else flask.request.form
