import copy

from common_core.base.util_base import UtilBase
from .object_utils.convert_object import ConvertObject


class ObjectUtil(UtilBase):

    @classmethod
    def print_object(cls, obj: object):
        """格式化输出对象"""
        obj = cls.format_object(obj)
        print(ConvertObject.object_to_str(obj))

    @staticmethod
    def format_object(obj: object) -> object:
        """格式化对象"""
        return ConvertObject.format_object(copy.deepcopy(obj))
