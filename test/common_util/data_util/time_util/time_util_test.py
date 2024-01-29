import datetime

from common_core.base.test_base import TestBase
from common_util.data_util.time_util.time_util import TimeUtil


class TimeUtilTestCase(TestBase):

    def setUp(self):
        self.stamp = datetime.datetime.now()

    def test_get_last_month_first_day(self):
        datetime_stamp = TimeUtil.get_last_month_first_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_last_month_last_day(self):
        datetime_stamp = TimeUtil.get_last_month_last_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_next_month_first_day(self):
        datetime_stamp = TimeUtil.get_next_month_first_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_next_month_last_day(self):
        datetime_stamp = TimeUtil.get_next_month_last_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_this_month_first_day(self):
        datetime_stamp = TimeUtil.get_this_month_first_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_this_month_last_day(self):
        datetime_stamp = TimeUtil.get_this_month_last_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_year_between_dates(self):
        from_date = datetime.datetime(2000, 1, 1)
        to_date = datetime.datetime.now()
        year = TimeUtil.get_year_between_dates(from_date, to_date)
        self.assertNotEqual(year, None)
        print(year)

    def test_format_time(self):
        time_str = TimeUtil.format_time(str(self.stamp))
        print(time_str)
