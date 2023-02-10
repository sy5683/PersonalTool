from personal_tool.base.tool_base import ToolBase
from personal_tool.ff14.battlefield_calendar.entity.battlefield_type import BattlefieldType
from personal_tool.ff14.battlefield_calendar.entity.custom_calendar import CustomCalendar


class BattlefieldCalendar(ToolBase):
    """
    战场日历
    1. 根据当前环境将战场类型作为可配置项（因为之前出现过一次增加战场【草原】的情况）
    2. 战场轮换频率为24小时，每天23点更新
    3. 需要将战场按当月日历的形式展现出来
    4. 需要展示当前战场与当天更新之后的战场
    """

    def __init__(self):
        self.custom_calendar = CustomCalendar(2)

    def main(self, check_battlefield_type: BattlefieldType = None):
        if check_battlefield_type is not None:
            self.custom_calendar.check_revision(check_battlefield_type)
        self.custom_calendar.show_calendar()
        day_battlefield = self.custom_calendar.get_now_day_battlefield()
        day_battlefield.show()


if __name__ == '__main__':
    battlefield_calendar = BattlefieldCalendar()
    battlefield_calendar.main()
