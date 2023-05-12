from typing import Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import WorkExperience


class Work002(WorkExperience):

    def get_company_name(self) -> str:
        """获取公司名称"""
        return "湖南大唐先一科技有限公司"

    def get_job_position(self) -> str:
        """获取职位"""
        return "Python开发工程师"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020年08月", "至今"

    def get_profile(self) -> str:
        """获取简介"""
        return "在该公司主要负责的项目是RPA机器人，本人主要负责的部分是所有脚本的开发实现工作。" \
               "自进入公司以来，在该公司接触过林林总总近四十种业务需求，开发过各种情况的场景。"

    def get_work_details(self) -> tuple:
        """获取工作明细"""
        return "在该公司接触了大量的场景，为财务处理过各式各样的问题，包括但不限于财务数据收集、自动制单填表、指定格式文件绘制等。", \
            "熟悉html解析与xpath编写，爬取过大量网站数据，包括但不限于公司网站与各种外部网站（政府网站、物资网站、招标网站等）。"
