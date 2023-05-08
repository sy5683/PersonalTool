from abc import ABCMeta, abstractmethod
from typing import List, Tuple


class ExperienceBase(metaclass=ABCMeta):

    def __init__(self):
        self.from_date, self.to_date = self.get_date_range()  # 开始时间 和 结束时间
        self.profile = self.get_profile()  # 简介

    @abstractmethod
    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""

    @abstractmethod
    def get_profile(self) -> str:
        """获取简介"""


class WorkExperience(ExperienceBase):

    def __init__(self):
        self.company_name = self.get_company_name()  # 公司名称
        super().__init__()

    @abstractmethod
    def get_company_name(self) -> str:
        """获取公司名称"""

    @abstractmethod
    def get_job_position(self) -> str:
        """获取职位"""


class ProjectExperience(ExperienceBase):

    def __init__(self):
        self.project_name = self.get_project_name()  # 项目名称
        super().__init__()
        self.project_details = self.get_project_details()  # 项目明细

    @abstractmethod
    def get_project_name(self) -> str:
        """获取项目名称"""

    @abstractmethod
    def get_technologies(self) -> List[str]:
        """获取开发技术"""

    @abstractmethod
    def get_project_details(self) -> tuple:
        """获取项目明细"""
