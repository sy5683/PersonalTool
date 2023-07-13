from ..base.event_base import EventBase
from ..role.纱鸠晴栖 import ShaJiuQingXi


class WenQuanShanZhuangBianTaiChuMoShiJian(EventBase):

    def set_event_info(self):
        self.name = "温泉山庄变态出没事件"
        self.is_done = False
        self.key_roles = [ShaJiuQingXi()]
