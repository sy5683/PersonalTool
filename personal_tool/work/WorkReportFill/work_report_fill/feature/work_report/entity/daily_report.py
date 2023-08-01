class DailyReport:
    """日报"""

    def __init__(self):
        self.date = None  # 日期
        self.today_work = None  # 今日工作
        self.tomorrow_plan = None  # 明日计划

    def to_report(self) -> str:
        return f"【{self.date}】\n今日内容：\n{self.today_work}\n明日计划：\n{self.tomorrow_plan}"
