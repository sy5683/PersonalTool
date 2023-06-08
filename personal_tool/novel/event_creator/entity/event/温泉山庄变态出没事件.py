from personal_tool.novel.event_creator.base.event import Event
from personal_tool.novel.event_creator.entity.role.纱鸠晴栖 import ShaJiuQingXi


class WenQuanShanZhuangBianTaiChuMoShiJian(Event):

    def set_event_info(self):
        self.name = "温泉山庄变态出没事件"
        self.is_done = False
        self.key_roles = [ShaJiuQingXi()]
