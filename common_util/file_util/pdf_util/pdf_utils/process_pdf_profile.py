import re
import typing

from .entity.pdf_element import Word
from .entity.pdf_profile import PdfProfile, ReceiptProfile


class ProcessPdfProfile:

    @classmethod
    def filter_word(cls, words: typing.List[Word], pattern: typing.Union[str, typing.Pattern[str]],
                    index: int) -> typing.Union[str, None]:
        """筛选文字"""
        try:
            return cls.filter_words(words, pattern)[index]
        except IndexError:
            return None

    @staticmethod
    def filter_words(words: typing.List[Word], pattern: typing.Union[str, typing.Pattern[str]]) -> typing.List[str]:
        """筛选文字列表"""
        pattern = re.compile(pattern) if isinstance(pattern, str) else pattern
        return [pattern.search(word.text).group(1) for word in words if pattern.search(word.text)]

    @classmethod
    def split_pdf(cls, pdf_profile: PdfProfile, *split_words: str) -> typing.List[ReceiptProfile]:
        """分割pdfpdf"""
        if not pdf_profile.tables:
            return cls.__split_pdf_without_table(pdf_profile, *split_words)
        # 获取pdf中所有表格坐标
        table_rects = [table.rect for table in pdf_profile.tables]
        # 根据表格坐标提取表格之间的间隔纵坐标
        ys = [(table_rects[index - 1][3], table_rects[index][1]) for index in range(1, len(table_rects))]
        # 将所有表格外的文本根据纵坐标进行分组
        all_interval_words = []
        for y in ys:
            interval_words = [word for word in pdf_profile.words if word.rect[3] > y[0] and word.rect[1] < y[1]]
            all_interval_words.append(interval_words)
        if not all_interval_words:
            return cls.__split_pdf_without_word(pdf_profile)
        # 获取间隔最大的两个word之间的纵坐标
        split_ys = []
        for interval_words in all_interval_words:
            max_interval_y = 0
            split_y = 0
            for index in range(len(interval_words)):
                interval_y = interval_words[index].rect[1] - interval_words[index - 1].rect[3]
                if interval_y < max_interval_y:
                    continue
                max_interval_y = interval_y
                split_y = (interval_words[index].rect[1] + interval_words[index - 1].rect[3]) // 2
            if split_y:
                split_ys.append(split_y)
        if not any(split_ys):
            return [ReceiptProfile(table) for table in pdf_profile.tables]
        split_ys = [0] + split_ys + [999999]
        # 根据纵坐标分割pdf
        receipt_profiles = []
        for index in range(1, len(split_ys)):
            receipt_profile = ReceiptProfile()
            for table in pdf_profile.tables:
                if table.rect[1] > split_ys[index - 1] and table.rect[3] < split_ys[index]:
                    assert receipt_profile.table is None, "异常格式，一个pdf判断出来多个表格"
                    receipt_profile.table = table
            for word in pdf_profile.words:
                if word.rect[1] > split_ys[index - 1] and word.rect[3] < split_ys[index]:
                    receipt_profile.words.append(word)
            receipt_profiles.append(receipt_profile)
        return receipt_profiles

    @classmethod
    def merge_words(cls, words: typing.List[Word], threshold: int) -> typing.List[Word]:
        """合并pdf文字"""
        new_words = []
        for index, word in enumerate(words):
            if index == 0:
                new_words.append(word)
                continue
            for last_word in new_words:
                if ((abs(word.rect[0] - last_word.rect[2]) > threshold)
                        or (abs(last_word.rect[0] - word.rect[2]) < threshold)):
                    continue
                if word.rect[1] > last_word.rect[3]:
                    continue
                last_word.update_rect((min(word.rect[0], last_word.rect[0]), min(word.rect[1], last_word.rect[1]),
                                       max(word.rect[2], last_word.rect[2]), max(word.rect[3], last_word.rect[3])))
                last_word.text += word.text
                break
            else:
                new_words.append(word)
        return new_words

    @staticmethod
    def __split_pdf_without_table(pdf_profile: PdfProfile, *split_words: str) -> typing.List[ReceiptProfile]:
        """切割没有表格的pdf"""
        if not split_words:
            return [ReceiptProfile(None, pdf_profile.words)]
        else:
            receipt_profiles = []
            receipt_profile = ReceiptProfile()
            for index, word in enumerate(pdf_profile.words):
                if re.search("|".join(split_words), word.text):
                    receipt_profile = ReceiptProfile()
                    receipt_profiles.append(receipt_profile)
                receipt_profile.words.append(word)
            return [receipt_profile for receipt_profile in receipt_profiles if len(receipt_profile.words) != 1]

    @staticmethod
    def __split_pdf_without_word(pdf_profile: PdfProfile) -> typing.List[ReceiptProfile]:
        """切割没有表格外文字的pdf"""
        if len(pdf_profile.tables) > 1:
            return [ReceiptProfile(table) for table in pdf_profile.tables]
        else:
            return [ReceiptProfile(pdf_profile.tables[0], pdf_profile.words)]
