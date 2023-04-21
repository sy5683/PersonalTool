from typing import List, Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import ProjectExperience


class Project002(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "APP与小程序的自动化测试"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2019-12", "2020-06"

    def get_profile(self) -> str:
        """获取简介"""
        return "为了保证公司App的稳定性，提升测试效率，定制公司APP与小程序专门的自动化测试脚本。" \
               "保证每天对程序进行测试，并将相应结果报告发送至部门邮箱。"

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["Appium"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return "对APP软件流程进行整体分析，根据流程设计对应的测试脚本，并设计对应的测试结果报告。", \
            "每日进行指定的版本测试，统计测试结果与失败样例数量，根据日志进行相应的结果分析。", \
            "需要将每日生成的测试结果与测试报告在下班前定时发送至部门邮箱。", \
            "在软件每次迭代升级时都要根据升级内容优化测试脚本，时时跟进。"
