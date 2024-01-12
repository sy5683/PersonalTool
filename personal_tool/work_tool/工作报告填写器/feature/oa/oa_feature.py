import time

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from ..work_report.entity.daily_report import DailyReport


class OaFeature:

    @staticmethod
    def login_oa():
        """登录OA"""
        name = "解劲松"
        username = "xiejinsong"
        password = "SYggdd_947"
        SeleniumUtil.open_url("http://10.50.144.123:8989/")
        SeleniumUtil.input('//input[@placeholder="用户名"]', username)
        SeleniumUtil.input('//input[@placeholder="密码"]', password)
        SeleniumUtil.click('//button/span[text()="登录"]')
        SeleniumUtil.find(f'//a[@id="navbar-right"]/span[text()="{name}"]')

    @staticmethod
    def fill_report(daily_report: DailyReport):
        """填写报告"""
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

    @staticmethod
    def submit_report():
        """提交报告"""
        SeleniumUtil.click('//input[@type="button" and @value="确定"]')
