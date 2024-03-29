import typing

from ...base.experience_base import ProjectExperience


class Project003(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "接口检测脚本开发"

    def get_work_character(self) -> str:
        """获取工作角色"""
        return "Python开发工程师"

    def get_date_range(self) -> typing.Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020年04月", "2020年04月"

    def get_profile(self) -> str:
        """获取简介"""
        return "因为打印机调用接口报错时无法将错误及时反馈，因为了在接口出现异常时第一时间发现问题，开发定时检测接口的脚本，并返回告警邮件给项目经理。"

    def get_technologies(self) -> typing.List[str]:
        """获取开发技术"""
        return ["Selenium"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return "通过爬虫爬取公司文档库地址，获取文档中所有接口文档，将获取的接口进行清洗，并自动写入公司文档库新网址中。", \
            "实现爬虫，每天早上上班之前模拟请求自动调用接口进行检测，并将有异常的接口整理出来自动发送告警邮件。"
