from typing import List, Tuple

from personal_tool.local_file.resume_creator.base.experience_base import ProjectExperience


class Project002(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "APP与小程序的自动化测试"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2019-12", "2020-06"

    def get_profile(self) -> str:
        """获取简介"""
        return "为了保证公司App的稳定性"

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["Appium", "Selenium"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return ""

    """APP与小程序的自动化测试 | 2019.12-2020.06
项目介绍：为了保证公司app的稳定性，保证在每次更新代码之后不影响老功能，开发对应的app与小程序的自动化测试脚本，保证每天进行一次测试并将相应结果报告发送至部门邮箱。
开发工具：Python、PyCharm、appium、selenium
开发技术：appium、selenium
负责内容：
o	对于整体APP系统流程分析、测试样例的分析与设计，根据测试样例设计测试报告与相应测试代码思路。
o	根据系统流程，实现相应整体的自动化测试代码脚本，并将结果统一输入测试报告中，统计每日的测试数量与失败样例数量，再根据日志进行相应的结果分析，并每日定时将结果统计与报告添加进邮件发送报告。
"""
