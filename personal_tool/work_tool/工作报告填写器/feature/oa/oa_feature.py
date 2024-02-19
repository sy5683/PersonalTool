import logging
import time
import typing

from selenium.common import TimeoutException

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ..work_report.entity.daily_report import DailyReport


class OaFeature:

    @staticmethod
    def login_oa():
        """登录OA"""
        username = "xiejinsong"
        password = "SYggdd_947"
        SeleniumUtil.open_url("http://10.50.144.123:8989/")
        SeleniumUtil.exist('//form[@autocomplete="off"]')
        try:
            SeleniumUtil.click('//div[@class="username"]/div[@class="img"]', wait_seconds=3)
        except TimeoutException:
            pass
        SeleniumUtil.input('//input[@placeholder="用户名"]', username)
        SeleniumUtil.input('//input[@placeholder="密码"]', password)
        SeleniumUtil.click('//button/span[text()="登录"]')
        SeleniumUtil.find(f'//div[@id="navbar-header"]')

    @staticmethod
    def switch_in_report_page():
        """切换至日报界面"""
        SeleniumUtil.click('//li[contains(@class, "ant-menu-item")]//span[text()="项目管理"]')
        SeleniumUtil.click('//div[@class="ant-menu-submenu-title"]//span[text()="项目计划管理"]')
        SeleniumUtil.click('//span[@class="spanhide" and text()="项目个人任务"]')

    @classmethod
    def fill_reports(cls, daily_reports: typing.List[DailyReport]):
        """填写报告"""
        for daily_report in daily_reports:
            if not daily_report.today_work:
                logging.warning(f"{daily_report.date}无日志")
                break
            if TimeUtil.format_time(daily_report.date, time_format='%m') != TimeUtil.get_now(time_format='%m'):
                logging.warning(f"当前日志不为当月日志，跳过: {daily_report.date}")
                continue
            cls._fill_report(daily_report)
        else:
            # 提交报告
            SeleniumUtil.click('//input[@type="button" and @value="确定"]')

    @staticmethod
    def _fill_report(daily_report: DailyReport):
        """填写报告"""
        logging.info(f"填写日报: {daily_report.date}")
        SeleniumUtil.switch_iframe('//iframe[@class="J_iframe  mainShow"]')
        SeleniumUtil.click('//a[text()="填写进度"]')
        SeleniumUtil.switch_iframe()
        SeleniumUtil.switch_iframe('//iframe[@name="t_dialog2"]')
        SeleniumUtil.input('//input[@id="workDate"]', daily_report.date, uncheck=True)
        SeleniumUtil.input('//input[@id="completionRadio"]', daily_report.completion_rate)
        SeleniumUtil.input('//input[@id="workingHoursNormal"]', 7.5)
        SeleniumUtil.input('//textarea[@id="workContent"]', daily_report.to_report())
        SeleniumUtil.switch_iframe()
        SeleniumUtil.click('//input[@type="button" and @value="保存"]')
        time.sleep(1)  # 防止意外，操作结束后强制等待一秒
