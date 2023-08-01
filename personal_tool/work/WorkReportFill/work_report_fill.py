from personal_tool.work.WorkReportFill.work_report_fill.feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFill:
    """工作报告填写"""

    def main(self):
        # 获取当前周报
        weekly_report = WorkReportFeature.get_now_weekly_report()
        for daily_report in weekly_report.daily_reports:
            print(daily_report.to_report())


if __name__ == '__main__':
    work_report_fill = WorkReportFill()
    work_report_fill.main()
