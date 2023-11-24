import datetime
import typing
from enum import Enum


class TimeFormat(Enum):
    """日期格式"""
    date = {'format': "%Y-%m-%d"}

    def to_format(self) -> str:
        return self.value['format']


class TimeUtil:

    @classmethod
    def get_now(cls, time_format: TimeFormat = TimeFormat.date) -> typing.Union[datetime.datetime, str]:
        """获取当前时间"""
        now_stamp = datetime.datetime.now()
        return cls.stamp_to_str(now_stamp, time_format)

    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    @staticmethod
    def stamp_to_str(time_stamp: typing.Union[str, datetime.datetime], time_format: TimeFormat = TimeFormat.date) -> str:
        """时间戳格式化为字符串"""
        return time_stamp.strftime(time_format.to_format()).format(Y="年", m="月", d="日", H="时", M="分", S="秒")
