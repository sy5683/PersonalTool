import typing

from .match_image import MatchImage


class MatchImageLinux(MatchImage):

    @classmethod
    def get_window_rect(cls, handle: int) -> typing.Tuple[int, int, int, int]:
        """获取窗口坐标"""
        raise Exception("Linux暂不支持模板匹配")
