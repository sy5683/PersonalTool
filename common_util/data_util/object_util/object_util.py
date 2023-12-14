import copy

from .object_utils.convert_object import ConvertObject


class ObjectUtil:

    @classmethod
    def print_object(cls, obj: object):
        """格式化输出对象"""
        obj = cls.format_object(obj)
        print(ConvertObject.object_to_str(obj))

    @staticmethod
    def format_object(obj: object) -> object:
        """格式化对象"""
        return ConvertObject.format_object(copy.deepcopy(obj))
