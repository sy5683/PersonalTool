import unittest
from enum import Enum

from common_util.data_util.object_util.object_util import ObjectUtil


class TestEnum(Enum):
    test = "测试"


class TestClass:
    def __init__(self):
        self.name = {TestEnum.test: "测试类"}


class ObjectUtilTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = {TestEnum: TestClass()}

    def test_print_object(self):
        ObjectUtil.print_object(self.obj)

    def test_format_object(self):
        obj = ObjectUtil.format_object(self.obj)
        print(type(obj), obj)
