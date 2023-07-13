from abc import ABCMeta, abstractmethod


class ToolBase(metaclass=ABCMeta):
    """工具基类"""

    def __init__(self, tool_name: str = ''):
        self.tool_name = tool_name  # 工具名称

    @abstractmethod
    def main(self):
        """主进程"""
