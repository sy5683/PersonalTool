import abc


class ExceptionBase(Exception, metaclass=abc.ABCMeta):
    """所有异常基类"""

    @property
    def brief_error_message(self):
        """获取错误信息，你可以自定义其他任何异常，只要实现了此方法，都能够在客户端显示你指定的错误信息"""
        return str(self)


class ErrorException(ExceptionBase):
    """通用异常报错"""


class FileFindError(ExceptionBase):
    """查找文件失败"""


class HandleDisappearOutTime(ExceptionBase):
    """句柄消失超时"""


class HandleFindError(ExceptionBase):
    """查找元素失败"""
