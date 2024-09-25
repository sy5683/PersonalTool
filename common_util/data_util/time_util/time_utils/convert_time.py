import datetime
import logging
import re
import typing


class ConvertTime:

    @classmethod
    def format_to_datetime(cls, stamp: typing.Union[datetime.datetime, datetime.date, float, str]) -> datetime.datetime:
        """格式化为datetime"""
        if isinstance(stamp, float):
            stamp = cls._time_to_datetime(stamp)
        if isinstance(stamp, str):
            stamp = cls._str_to_datetime(stamp)
        return stamp

    @classmethod
    def format_to_str(cls, stamp: typing.Union[datetime.datetime, datetime.date, float, str], time_format: str) -> str:
        """格式化为字符串"""
        try:
            stamp = cls.format_to_datetime(stamp)
            return cls._datetime_to_str(stamp, time_format)
        except AttributeError:  # 日期为空时
            return ""
        except Exception as e:
            logging.warning(e)
            return ""

    @staticmethod
    def _datetime_to_str(stamp: typing.Union[datetime.datetime, datetime.date], time_format: str) -> str:
        """datetime转字符串"""
        return stamp.strftime(time_format).format(Y='年', m='月', d='日', H='时', M='分', S='秒')

    @staticmethod
    def _str_to_datetime(stamp: str) -> datetime.datetime:
        """字符串转时间戳"""
        try:
            # 提取字符串中的数字并补零
            datetime_number = "".join([each.zfill(2) for each in re.findall(r"\d+", stamp)])
            assert len(datetime_number) >= 6  # 格式最少要有年月
        except (AssertionError, TypeError):
            raise ValueError(f"时间异常，无法格式化: {stamp}")
        if len(datetime_number) == 6:
            datetime_number += "01"  # 补上日期，默认1号
        datetime_number = datetime_number.ljust(14, "0")[:14]  # 补上时间，使其变为14位时间数字
        return datetime.datetime.strptime(datetime_number, "%Y%m%d%H%M%S")

    @staticmethod
    def _time_to_datetime(stamp: float) -> datetime.datetime:
        """时间戳转datetime，时间戳目前只有10位（秒级）和13位（毫秒级）两种"""
        if len(str(int(stamp))) == 13:
            stamp = stamp / 1000
        return datetime.datetime.fromtimestamp(stamp)
