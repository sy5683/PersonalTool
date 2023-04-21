from ...base.event import Event
from ...entity.role.纱鸠晴栖 import ShaJiuQingXi


class WenQuanShanZhuangBianTaiChuMoShiJian(Event):

    def set_event_info(self):
        self.is_done = False
        self.name = "温泉山庄变态出没事件"
        self.key_roles = [ShaJiuQingXi()]
