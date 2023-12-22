class DailyReport:
    """日报"""

    def __init__(self):
        self.date = None  # 日期
        self.today_work = None  # 今日工作
        self.tomorrow_plan = None  # 明日计划
        self.completion_rate = None  # 完成率

    def to_report(self) -> str:
        return f"今日内容：\n{self.today_work}\n明日计划：\n{self.tomorrow_plan}"
