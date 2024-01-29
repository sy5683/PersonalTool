import abc
import logging
import sys
import time
import unittest
from pathlib import Path


class TestBase(unittest.TestCase, metaclass=abc.ABCMeta):
    """测试基类"""
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None,
                        filemode='a')

    def get_test_file(self, file_name: str = None) -> Path:
        """获取测试用的文件路径（测试代码同级目录）"""
        test_file = Path(sys.modules[self.__module__].__file__)
        if file_name:
            test_file = test_file.parent.joinpath(file_name)
        return test_file

    def __del__(self):
        # 结尾强制等待0.01秒，保证控制台打印的信息保留在一起
        try:
            time.sleep(0.01)
        except OSError:
            pass
