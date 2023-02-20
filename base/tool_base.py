from abc import ABCMeta, abstractmethod


class ToolBase(metaclass=ABCMeta):
    """工具基类"""

    @abstractmethod
    def main(self):
        """主进程"""
