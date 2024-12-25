
from ..base.controller_base import ControllerBase
from ...file_feature import FileFeature


class Github(ControllerBase):

    def submit(self):
        """提交项目"""
        image_path = FileFeature.get_image_path("github/main.png")
        print(image_path)
        print("提交项目")

    def update(self):
        """更新项目"""
        image_path = FileFeature.get_image_path("github/main.png")
        print(image_path)
        print("更新项目")
