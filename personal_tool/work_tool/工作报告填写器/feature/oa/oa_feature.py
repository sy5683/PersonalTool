import logging
import time
import typing

from selenium.common import TimeoutException

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from ..work_report.entity.daily_report import DailyReport


class OaFeature:

    @staticmethod
    def login_oa():
        """登录OA"""
        name = "解劲松"
        username = "xiejinsong"
        password = "SYggdd_947"
        logging.info(f"登录OA系统: {name}")
        SeleniumUtil.open_url("http://10.50.144.123:8989/")
        SeleniumUtil.exist('//form[@autocomplete="off"]')
        try:
            SeleniumUtil.click('//div[@class="username"]/div[@class="img"]', wait_seconds=3)
        except TimeoutException:
            pass
        SeleniumUtil.input('//input[@placeholder="用户名"]', username)
        SeleniumUtil.input('//input[@placeholder="密码"]', password)
        SeleniumUtil.click('//button/span[text()="登录"]')
        SeleniumUtil.find(f'//a[@id="navbar-right"]/span[text()="{name}"]')

    @staticmethod
    def switch_in_report_page():
        """切换至日报界面"""
        SeleniumUtil.click('//li[contains(@class, "ant-menu-item")]//span[text()="项目管理"]')
        SeleniumUtil.click('//div[@class="ant-menu-submenu-title"]//span[text()="项目计划管理"]')
        SeleniumUtil.click('//span[@class="spanhide" and text()="项目个人任务"]')

    @staticmethod
    def fill_report(daily_reports: typing.List[DailyReport]):
        """填写报告"""
        for daily_report in daily_reports:
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
        # 提交报告
        SeleniumUtil.click('//input[@type="button" and @value="确定"]')
