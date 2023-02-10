import datetime
from typing import List

from personal_tool.ff14.battlefield_calendar.entity.battlefield_type import BattlefieldType
from personal_tool.ff14.battlefield_calendar.entity.day_battlefield import DayBattlefield
from personal_tool.ff14.battlefield_calendar.feature.calendar_feature import CalendarFeature


class CustomCalendar:

    def __init__(self, revision: int):
        """自定义日历类"""
        self.revision = revision
        self.now = datetime.datetime.now()
        self.calendar_list: List[DayBattlefield] = []
        self.get_calendar_list()

    def get_now_day_battlefield(self) -> DayBattlefield:
        for day_battlefield in self.calendar_list:
            if day_battlefield.date == self.now.date():
                return day_battlefield

    def show_calendar(self):
        print(f"==========================================")
        calendar_table: List[List[DayBattlefield]] = self._cut_calendar_list(7)
        for week_battlefields in calendar_table:
            date_show = []
            battlefields = []
            for day_battlefield in week_battlefields:
                date_show.append(f"{str(day_battlefield.date.day).zfill(2)}　　")
                battlefields.append(day_battlefield.battlefield_type.to_sign())
            print(" " + " ".join(date_show))
            print("   ".join(battlefields))
        print(f"==========================================")

    def check_revision(self, battlefield_type: BattlefieldType):
        """确认修正天数"""
        new_revision = (self.now.day + battlefield_type.to_index() + 2) % 4
        if self.revision != new_revision:
            print(f"==========【revision】应该修改为: {new_revision}==========")
            self.revision = new_revision
            self.calendar_list = []
            self.get_calendar_list()

    def get_calendar_list(self):
        """获取日历表格"""
        calendar_list = CalendarFeature.get_calendar_list(self.now.year, self.now.month)
        for index, day in enumerate(calendar_list):
            day_battlefield = DayBattlefield(day)
            day_battlefield.set_battlefield_type(BattlefieldType.get_enum_by_index(index, self.revision))
            day_battlefield.set_next_battlefield_type(BattlefieldType.get_enum_by_index(index + 1, self.revision))
            self.calendar_list.append(day_battlefield)

    def _cut_calendar_list(self, cut_len: int) -> list:
        """切割列表"""
        group_listing = zip(*(iter(self.calendar_list),) * cut_len)
        cut_listing = [list(listing) for listing in group_listing]
        cut_count = len(self.calendar_list) % cut_len
        cut_listing.append(self.calendar_list[-cut_count:]) if cut_count != 0 else cut_listing
        return cut_listing
