from ...角色.纱鸠晴栖 import ShaJiuQingXi
from .....feature.entity.event import Event


class WenQuanShanZhuangBianTaiChuMoShiJian(Event):

    def set_event_info(self):
        """设置事件信息"""
        self.is_done = False
        self.key_roles = [ShaJiuQingXi()]
