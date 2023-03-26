from typing import Tuple

from personal_tool.local_file.resume_creator.base.experience_base import ProjectExperience


class Project001(ProjectExperience):

    def get_project_name(self) -> str:
        return "阅卷系统的图像处理相关支持"

    def get_date_range(self) -> Tuple[str, str]:
        return "2019-09", "2019-12"

    def get_profile(self) -> str:
        return "该项目是基于公司项目“阅卷系统”的OCR相关支持。" \
               "为了满足公司需求，提升识别准确度并降低调用接口的费用，在调用百度OCR接口之前"
