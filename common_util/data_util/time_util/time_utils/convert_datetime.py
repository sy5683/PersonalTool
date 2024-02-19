import datetime
import re
import typing

from .time_config import TimeConfig


class ConvertDatetime:

    @classmethod
    def format_time(cls, time_str: str, **kwargs) -> str:
        """格式时间"""
        time_format = kwargs.get("time_format", TimeConfig.default_time_format)
        stamp = cls._str_to_datetime(time_str)
        return cls._datetime_to_str(stamp, time_format)

    @staticmethod
    def _datetime_to_str(stamp: typing.Union[datetime.datetime, datetime.date], time_format: str) -> str:
        """
        时间戳格式化为字符串
        中文格式必须为: %Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}
        """
        return stamp.strftime(time_format).format(Y='年', m='月', d='日', H='时', M='分', S='秒')

    @staticmethod
    def _str_to_datetime(datetime_str: str) -> datetime.datetime:
        """字符串转时间戳"""
        if datetime_str is None:
            datetime_str = ""
        datetime_str = "".join([each.zfill(2) for each in re.findall(r"\d+", datetime_str)])
        datetime_number = re.sub(r"\D+", "", datetime_str)
        if len(datetime_number) < 6:
            return datetime.datetime.now()
        elif len(datetime_number) == 6:
            datetime_number += "01000000"  # 补上日期，默认1号
        else:
            datetime_number = datetime_number.ljust(14, "0")[:14]  # 补上时间，使其变为14位时间数字
        return datetime.datetime.strptime(datetime_number, "%Y%m%d%H%M%S")
