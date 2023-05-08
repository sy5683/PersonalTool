from typing import Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import WorkExperience


class Work001(WorkExperience):

    def get_company_name(self) -> str:
        """获取公司名称"""
        return "湖南诚和达科技有限公司"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2019年09月", "2020年06月"

    def get_profile(self) -> str:
        """获取简介"""
        return "在该公司主要负责python的相关开发。" \
               "主要负责的项目有OCR识别与图像处理的支持工作、选择题与判断题识别订制开发，app与小程序的自动化脚本开发，以及自动化测试脚本开发。"

    def get_job_position(self) -> str:
        """获取职位"""
        return "Python开发工程师"
