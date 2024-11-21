import flask

from .flask_utils.flask_init import FlaskInit
from .flask_utils.flask_parameter import FlaskParameter


class FlaskUtil:

    @staticmethod
    def get_app(name: str = '') -> flask.app:
        """获取app服务"""
        return FlaskInit.get_app(name)

    @staticmethod
    def get_json(key: str = '') -> any:
        """获取json参数"""
        return FlaskParameter.get_json(key)

    @staticmethod
    def get_kwarg(key: str = '') -> any:
        """获取参数"""
        return FlaskParameter.get_kwarg(key)

    @staticmethod
    def run(app: flask.app, port: int = 8080):
        """运行接口"""
        app.run(host="0.0.0.0", port=port, threaded=True)
