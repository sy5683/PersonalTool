from typing import Tuple

from personal_tool.local_file.resume_creator.base.experience_base import ProjectExperience


class Project001(ProjectExperience):

    def get_project_name(self) -> str:
        return "阅卷系统的图像处理相关支持"

    def get_date_range(self) -> Tuple[str, str]:
        return "2019-09", "2019-12"
