import typing


class FlaskResponse(object):

    def __init__(self, code: int = 0, data: typing.Any = '', message: str = ''):
        self.code = code
        self.data = data
        self.message = message

    def to_dict(self):
        if not self.code:
            return {'code': self.code, 'data': self.data}
        else:
            return {'code': self.code, 'error_message': self.message}
