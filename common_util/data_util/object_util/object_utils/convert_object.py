import collections
import datetime
import json
import typing
from enum import Enum, EnumMeta
from pathlib import Path


class ConvertObject:

    @classmethod
    def format_object(cls, obj: object) -> object:
        """格式化对象"""
        if isinstance(obj, (datetime.datetime, datetime.date, Path)):
            return cls.format_object(str(obj))
        if isinstance(obj, (dict, collections.OrderedDict)):
            # 字典的键必须为不可变对象，因此需要对特殊情况进行处理
            obj = {key.name if isinstance(key, Enum) else key: value for key, value in obj.items()}
            obj = {key.__name__ if isinstance(key, EnumMeta) else key: value for key, value in obj.items()}
            return {cls.format_object(key): cls.format_object(value) for key, value in obj.items()}
        elif isinstance(obj, Enum):
            return cls.format_object({obj.name: obj.value})
        elif isinstance(obj, (list, tuple, set, EnumMeta, typing.Generator)):
            # 虽然这些对象转换为元组对象好点，但是因为该方法主要是用于格式化输出，而元组无法使用json格式print，因此这里还是返回列表
            return [cls.format_object(each) for each in obj]
        elif hasattr(obj, '__dict__'):
            return cls.format_object(obj.__dict__)
        elif cls._check_object_is_basic(obj):
            return obj
        else:
            raise ValueError(f"未识别的对象【{obj}】类型: {type(obj)}")

    @staticmethod
    def object_to_str(obj: object) -> str:
        """对象转字符串"""
        # ensure_ascii设置为False使转换时中文不会被转换为Unicode，indent表示输出时的缩进
        return json.dumps(obj, ensure_ascii=False, indent=2)

    @staticmethod
    def _check_object_is_basic(obj: object) -> bool:
        """判断对象是否为基本数据类型"""
        basic_object_types = (int, float, bool, complex, str, list, tuple, set, dict)  # isinstance多条件判断需要使用元组
        if obj is None or isinstance(obj, basic_object_types):
            return True
        return False
