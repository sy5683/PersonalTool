import pypinyin


class PinyinFeature:

    @staticmethod
    def chinese_to_object_name(chinese: str) -> str:
        """中文转英文拼音（没有音标）"""
        return "_".join(pypinyin.lazy_pinyin(chinese))
