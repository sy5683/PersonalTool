import datetime


class ConvertTime:

    @staticmethod
    def time_to_datetime(stamp: float) -> datetime.datetime:
        """时间戳转datetime，时间戳目前只有10位（秒级）和13位（毫秒级）两种"""
        if len(str(int(stamp))) == 13:
            stamp = stamp / 1000
        return datetime.datetime.fromtimestamp(stamp)
