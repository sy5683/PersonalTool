import logging
import time
import typing

from selenium import common

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.data_util.time_util.time_util import TimeUtil
from ..work_report.entity.daily_report import DailyReport


class OaFeature:

    @staticmethod
    def login_oa():
        """登录OA"""
        SeleniumUtil.launch_chrome_debug(9222)
        username = "xiejinsong"
        password = "SYggdd_947"
        SeleniumUtil.open_url(SeleniumConfig(), "http://10.50.144.123:8989/")
        SeleniumUtil.exist(SeleniumConfig(xpath='//form[@autocomplete="off"]'))
        try:
            SeleniumUtil.click(SeleniumConfig(xpath='//div[@class="username"]/div[@class="img"]', wait_seconds=3))
        except common.TimeoutException:
            pass
        SeleniumUtil.input(SeleniumConfig(xpath='//input[@placeholder="用户名"]'), username)
        SeleniumUtil.input(SeleniumConfig(xpath='//input[@placeholder="密码"]'), password)
        SeleniumUtil.click(SeleniumConfig(xpath='//button/span[text()="登录"]'))
        SeleniumUtil.find(SeleniumConfig(xpath=f'//div[@id="navbar-header"]'))

    @staticmethod
    def switch_in_report_page():
        """切换至日报界面"""
        SeleniumUtil.click(SeleniumConfig(xpath='//li[contains(@class, "ant-menu-item")]//span[text()="项目管理"]'))
        SeleniumUtil.click(SeleniumConfig(xpath='//div[@class="ant-menu-submenu-title"]//span[text()="项目计划管理"]'))
        SeleniumUtil.click(SeleniumConfig(xpath='//span[@class="spanhide" and text()="项目个人任务"]'))

    @classmethod
    def fill_reports(cls, daily_reports: typing.List[DailyReport]):
        """填写报告"""
        daily_report = DailyReport()
        for daily_report in daily_reports:
            if not daily_report.today_work:
                logging.warning(f"{daily_report.date}无日志")
                break
            if TimeUtil.format_to_str(daily_report.date, "%m") != TimeUtil.get_now("%m"):
                logging.warning(f"当前日志不为当月日志，跳过: {daily_report.date}")
                continue
            cls._fill_report(daily_report)
        if daily_report.completion_rate == 100:
            # 提交报告
            SeleniumUtil.click(SeleniumConfig(xpath='//input[@type="button" and @value="确定"]'))

    @staticmethod
    def _fill_report(daily_report: DailyReport):
        """填写报告"""
        logging.info(f"填写日报: {daily_report.date}")
        SeleniumUtil.switch_iframe(SeleniumConfig(xpath='//iframe[@class="J_iframe  mainShow"]'))
        SeleniumUtil.click(SeleniumConfig(xpath='//a[text()="填写进度"]'))
        SeleniumUtil.switch_iframe(SeleniumConfig())
        SeleniumUtil.switch_iframe(SeleniumConfig(xpath='//iframe[@name="t_dialog2"]'))
        SeleniumUtil.input(SeleniumConfig(xpath='//input[@id="workDate"]', check_input=False), daily_report.date)
        SeleniumUtil.input(SeleniumConfig(xpath='//input[@id="completionRadio"]'), daily_report.completion_rate)
        SeleniumUtil.input(SeleniumConfig(xpath='//input[@id="workingHoursNormal"]'), 7.5)
        SeleniumUtil.input(SeleniumConfig(xpath='//textarea[@id="workContent"]'), daily_report.to_report())
        SeleniumUtil.switch_iframe(SeleniumConfig())
        SeleniumUtil.click(SeleniumConfig(xpath='//input[@type="button" and @value="保存"]'))
        time.sleep(1)  # 防止意外，操作结束后强制等待一秒
