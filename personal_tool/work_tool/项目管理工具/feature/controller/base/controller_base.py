import abc


class ControllerBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def submit(self):
        """提交项目"""

    @abc.abstractmethod
    def update(self):
        """更新项目"""
