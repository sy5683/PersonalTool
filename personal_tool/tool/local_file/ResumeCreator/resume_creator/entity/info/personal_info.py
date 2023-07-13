from typing import List

from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class PersonalInfo(InfoBase):

    def __init__(self):
        super().__init__("个人信息")
        self.skills = [  # 个人技能
            "熟练使用Python，开发过各种场景，能满足各种场景开发需求。",
            "熟悉html和Xpath，能迅速对页面数据实现各种情况的定位与处理。",
            "熟练使用openCV与PIL等图像库，也会PS，能满足业务、代码方面对图片的处理需求。",
            "熟练使用openpyxl与docx，能协助实现各种各样办公室文档的解析与生成。",
        ]
        self.profile = "为人诚信，能吃苦耐劳，对工作认真负责，积极取进，时间观念强，勇于面对困难挑战。"  # 个人介绍

    def to_contexts(self) -> List[str]:
        """转换为文本"""
        return ["个人技能: "] + [f"\t· {skill}" for skill in self.skills] + [f"个人介绍: {self.profile}"]
