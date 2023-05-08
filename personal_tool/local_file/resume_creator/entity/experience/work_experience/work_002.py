from typing import Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import WorkExperience


class Work002(WorkExperience):

    def get_company_name(self) -> str:
        """获取公司名称"""
        return "湖南大唐先一科技有限公司"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020年08月", "至今"

    def get_profile(self) -> str:
        """获取简介"""
        return "在该公司主要负责的项目是RPA机器人，本人主要负责的部分是所有脚本的开发实现工作。" \
               "近三年时间，在该公司接触过林林总总近三十个场景，开发过各种情况的场景，其中使用的python库五花八门。"

    def get_job_position(self) -> str:
        """获取职位"""
        return "Python开发工程师"
