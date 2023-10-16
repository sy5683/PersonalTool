import typing

import jieba


class JiebaCut:

    def __init__(self):
        # 分词器添加自定义词语
        jieba.add_word("玊烨")

    @staticmethod
    def cut(string: str) -> typing.List[str]:
        return jieba.lcut(string)  # 精确模式

    @staticmethod
    def cut_for_search(string: str) -> typing.List[str]:
        return jieba.lcut_for_search(string)
