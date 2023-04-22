from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class IntentionInfo(InfoBase):

    def __init__(self):
        super().__init__("求职意向")
        self.job_position = "Python开发工程师"
        self.in_position_time = "一个月"

    def to_text(self) -> str:
        """转换为文本"""
        return f"求职岗位: {self.job_position}\t到岗时间: {self.in_position_time}"
