import typing

import pypinyin


class ConvertChinese:

    @classmethod
    def chinese_to_object_name(cls, chinese: str) -> str:
        """中文转对象名"""
        return "_".join(cls._chinese_to_english_pinyin(chinese))

    @staticmethod
    def _chinese_to_english_pinyin(chinese: str) -> typing.List[str]:
        """中文转英文拼音（没有音标）"""
        return pypinyin.lazy_pinyin(chinese)
