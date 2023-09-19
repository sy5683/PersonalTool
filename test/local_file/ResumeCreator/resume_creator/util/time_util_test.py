import datetime
import unittest

from personal_tool.personal.ResumeCreator.resume_creator.util.time_util import TimeUtil


class DateUtilTestCase(unittest.TestCase):

    def test_get_year_between_dates(self):
        from_date = datetime.datetime(2000, 1, 1)
        to_date = datetime.datetime.now()
        year = TimeUtil.get_year_between_dates(from_date, to_date)
        self.assertNotEqual(year, None)
        print(year)
