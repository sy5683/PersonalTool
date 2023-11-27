import datetime
import unittest

from common_util.data_util.time_util.time_util import TimeUtil


class TimeUtilTestCase(unittest.TestCase):

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

    def test_get_this_month_first_day(self):
        datetime_stamp = TimeUtil.get_this_month_first_day(self.stamp)
        self.assertNotEqual(datetime_stamp, None)
        print(datetime_stamp)

    def test_get_this_month_last_day(self):
        datetime_stamp = TimeUtil.get_this_month_last_day(self.stamp)
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

    def test_format_time(self):
        time_str = TimeUtil.format_time(str(self.stamp))
        print(time_str)
