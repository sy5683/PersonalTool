from ...角色.纱鸠晴栖 import ShaJiuQingXi

from .....entity.event import Event


class WenQuanShanZhuangBianTaiChuMoShiJian(Event):

    def _set_event_info(self):
        """设置事件信息"""
        self.is_done = False
        self.key_roles = [ShaJiuQingXi()]

    def _set_event_content(self):
        """设置正文"""
        self.title = "只有你努力在别人面前展示自己外貌以外的个人特点才能让别人对你做到不以貌取人"
        self.text = """
        """
