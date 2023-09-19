import unittest

from personal_util.time_util import TimeUtil, TimeFormat


class TimeUtilTestCase(unittest.TestCase):

    def test_get_now(self):
        now = TimeUtil.get_now(TimeFormat.full)
        self.assertNotEqual(now, None)
        print(now)
