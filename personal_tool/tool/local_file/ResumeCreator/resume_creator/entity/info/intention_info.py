from typing import List

from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class IntentionInfo(InfoBase):

    def __init__(self):
        super().__init__("求职意向")
        self.job_position = "Python开发工程师"  # 职位
        self.in_position_time = "一个月内"  # 入职时间
        self.salary_expectation = 12000  # 期望薪资

    def to_contexts(self) -> List[str]:
        """转换为文本"""
        return [f"求职岗位: {self.job_position}", f"期望薪资: {self.salary_expectation}",
                f"到岗时间: {self.in_position_time}"]
