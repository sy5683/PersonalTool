import datetime
import unittest

from personal_tool.local_file.resume_creator.util.date_util import DateUtil


class DateUtilTestCase(unittest.TestCase):

    def test_get_year_between_dates(self):
        from_date = datetime.datetime(2000, 1, 1)
        to_date = datetime.datetime.now()
        year = DateUtil.get_year_between_dates(from_date, to_date)
        self.assertNotEqual(year, None)
        print(year)
