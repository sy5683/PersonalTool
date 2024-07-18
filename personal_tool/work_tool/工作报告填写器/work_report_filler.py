import datetime

from common_core.base.tool_base import ToolBase
from common_util.data_util.time_util.time_util import TimeUtil
from feature.config import WorkReportFillerConfig
from feature.oa.oa_feature import OaFeature
from feature.work_report.work_report_feature import WorkReportFeature
from feature.date_feature import DateFeature


class WorkReportFiller(ToolBase):

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        target_date = TimeUtil.format_to_str(target_date, WorkReportFillerConfig.time_format)
        self.weekly_report = WorkReportFeature.get_weekly_report(target_date)

    def main(self, filling: bool = True):
        if filling and DateFeature.get_now_date() in self.weekly_report.date_range:
            # 1.1) 登录OA
            OaFeature.login_oa()
            # 1.2) 切换至日报界面
            OaFeature.switch_in_report_page()
            # 1.3) 填写工作报告
            OaFeature.fill_reports(self.weekly_report.daily_reports)
        else:
            # 2) 目标日志为历史日志，不为当周。因此只将日志输出，自己手填
            for daily_report in self.weekly_report.daily_reports:
                print(f"【{daily_report.date}】")
                print(daily_report.to_report())
                print()


if __name__ == '__main__':
    work_report_filler = WorkReportFiller()
    work_report_filler.main()

    """
"打包测试已实现的几个新版本公共组件，确认组件运行正常。
梳理selenium公共组件，实现浏览器驱动与rpa控制台的交互。
补充优化selenium公共组件自动下载驱动的功能。
查看薪酬分发场景线上反馈的bug。确认问题为前端谷歌浏览器的兼容问题。"	"以新版本公共组件框架，实现rpa控制台附件相关公共组件。
以新版本公共组件框架，实现银行流水解析公共组件。"
"查看薪酬分发场景的问题。
查看evs公共组件上传文件报错的问题。
以新版本公共组件框架，实现rpa控制台附件相关公共组件。
以新版本公共组件框架，实现银行流水解析公共组件。
测试银行流水解析公共组件是否正常运行，确认除农行格式外所有格式运行无误。"	实现财务共享接口获取农行账号的公共组件。
"实现自动更新selenium驱动至控制台的公共组件。
测试自动更新selenium驱动的公共组件是否成功运行。
查看学习版本与rpa版本的selenium源码区别，查找rpa无法连接服务器下载驱动的问题。
优化提取部分源码，对rpa版本selenium源码进行修改，使其可以支持在Windows和linux下的执行。
实现财务共享接口获取农行账号的公共组件。"	实现财务共享接口获取农行账号的公共组件，对其进行财务共享系统3.0和4.0的区分。
"测试已实现的几个公共组件在联动方面运行是否正常。
查看工行回单pdf解析异常的问题。
实现财务共享接口获取农行账号的公共组件。
实现自定义配置与在线配置的公共组件。
梳理优化实现公司业务环境相关的公共组件。"	梳理优化实现公司业务环境相关的公共组件。

    """
