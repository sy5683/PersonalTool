from abc import ABCMeta


class ExceptionBase(Exception, metaclass=ABCMeta):
    """所有异常基类"""

    @property
    def brief_error_message(self):
        """获取错误信息，你可以自定义其他任何异常，只要实现了此方法，都能够在客户端显示你指定的错误信息"""
        return str(self)


class ErrorException(ExceptionBase):
    """通用异常报错"""


class DisappearOutTime(ExceptionBase):
    """存在超时"""


class ElementFindError(ExceptionBase):
    """查找元素失败"""


class FileFindError(ExceptionBase):
    """未找到文件"""


class MatchError(ExceptionBase):
    """匹配失败"""
