import typing

from .entity.jieba_cut import JiebaCut


class JiebaFeature:
    _jieba_cut = None

    @classmethod
    def cut(cls, string: str) -> typing.List[str]:
        return cls._get_jieba_cut().cut(string)

    @classmethod
    def _get_jieba_cut(cls) -> JiebaCut:
        if cls._jieba_cut is None:
            cls._jieba_cut = JiebaCut()
        return cls._jieba_cut
