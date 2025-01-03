import abc
import time
import unittest
from pathlib import Path

from .log_base import LogBase


class TestBase(unittest.TestCase, LogBase, metaclass=abc.ABCMeta):
    """测试基类"""

    def get_test_file(self, file_name: str = None) -> Path:
        """获取测试用的文件路径（测试代码同级目录）"""
        return self.get_subclass_path(file_name)

    def tearDown(self):
        # 结尾强制等待0.01秒，保证控制台打印的信息保留在一起
        try:
            time.sleep(0.01)
        except OSError:
            pass
