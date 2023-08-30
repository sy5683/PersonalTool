from .....feature.entity.event import Event


class WenQuanShanZhuangBianTaiChuMoShiJian(Event):

    def __init__(self):
        super().__init__("温泉山庄变态出没事件")

    def set_event_info(self):
        """设置事件信息"""
        # self.is_done = False
        # self.key_roles = [ShaJiuQingXi()]
