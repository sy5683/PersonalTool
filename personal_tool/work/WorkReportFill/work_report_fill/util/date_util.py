import datetime


class DateUtil:

    @classmethod
    def get_now_date(cls) -> str:
        return cls.datetime_to_str(datetime.datetime.now())

    @staticmethod
    def datetime_to_str(datetime_stamp: datetime.datetime) -> str:
        return datetime_stamp.strftime("%Y-%m-%d")
