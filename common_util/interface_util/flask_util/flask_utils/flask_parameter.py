import flask


class FlaskParameter:

    @staticmethod
    def get_json(key: str) -> any:
        """获取json参数"""
        json_dict = flask.request.args.to_dict() if flask.request.method == "GET" else flask.request.get_json()
        return json_dict.get(key, json_dict)

    @staticmethod
    def get_kwarg(key: str) -> any:
        """获取参数"""
        kwargs = flask.request.args if flask.request.method == "GET" else flask.request.form
        return kwargs.get(key, kwargs)
