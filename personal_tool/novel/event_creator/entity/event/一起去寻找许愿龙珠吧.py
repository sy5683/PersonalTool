from personal_tool.novel.event_creator.base.event import Event
from personal_tool.novel.event_creator.entity.role.东方灵 import DongFangLing


class YiQiQuXunZhaoXuYuanLongZhu(Event):

    def set_event_info(self):
        self.name = "一起去寻找许愿龙珠吧"
        self.is_done = False
        self.key_roles = [DongFangLing()]
        """
        据说，在黑市中流传着龙珠，只要集齐龙珠，就可以实现任何愿望。
        他们分别是黄、绿、咖啡、蓝、粉、黑和白色珠。
        但是除了这七颗正品，还有15颗无法实现愿望的假货，这些龙珠在短暂实现简单的任务之后，就会变成红色。
        召唤神龙的方式有两种，最简单的是集齐七颗彩色龙珠，便可实现愿望，但是一次只能实现一个简单的愿望。
        第二种方式则是，在集齐七颗彩色龙珠的基础上，同时集齐剩余的15颗龙珠。
        然后将这22颗龙珠按规定的形状摆放，并拿到147分。
        这不就是斯诺克吗！！！
        """
