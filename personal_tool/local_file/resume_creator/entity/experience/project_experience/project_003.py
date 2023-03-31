

from typing import List, Tuple

from personal_tool.local_file.resume_creator.base.experience_base import ProjectExperience


class Project003(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "接口检测脚本"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020-04", "2020-04"

    def get_profile(self) -> str:
        """获取简介"""
        return ""

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["Selenium"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return ""
"""
项目介绍：为了在接口出现异常时能及时发现问题，能在第一时间处理，实现了定时检测接口的脚本， 并在接口有问题的时候自动生成邮箱发送告警。
开发工具：Python、PyCharm、appium、selenium
开发技术：appium、selenium
负责内容：
o	通过爬虫获取公司文档库网址中所有的接口文档，将所有的接口提取出来进行清洗。
o	为了便于公司员工对接口的添加修改，将清洗好的接口整理至公司文档库网站中，使用爬虫爬取文档获得数据进行检测。
o	将有异常的接口整理出来并入邮箱自动发送告警。
"""
