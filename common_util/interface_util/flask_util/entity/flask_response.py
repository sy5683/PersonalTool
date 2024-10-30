import typing


class FlaskResponse(object):

    def __init__(self, code: int = 0, data: typing.Any = '', message: str = ''):
        self.code = code
        self.data = data
        self.message = message

    def to_dict(self):
        return {
            'code': self.code,
            'data': self.data,
            'message': self.message
        }
