from abc import ABCMeta, abstractmethod
from typing import Tuple


class ExperienceBase(metaclass=ABCMeta):

    def __init__(self):
        self.from_date, self.to_date = self.get_date_range()  # 开始时间 和 结束时间
        self.profile = None  # 简介

    @abstractmethod
    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""


class WorkExperience(ExperienceBase):

    def __init__(self):
        self.company_name = self.get_company_name()  # 公司名称
        super().__init__()

    @abstractmethod
    def get_company_name(self):
        """获取公司名称"""


class ProjectExperience(ExperienceBase):

    def __init__(self):
        self.project_name = self.get_project_name()  # 项目名称
        super().__init__()

    @abstractmethod
    def get_project_name(self) -> str:
        """获取项目名称"""
