import typing

from .entity.pdf_profile import PdfProfile, ReceiptProfile


class ProcessPdfProfile:

    @staticmethod
    def split_receipt_pdf(pdf_profile: PdfProfile) -> typing.List[ReceiptProfile]:
        """分割回单pdf"""
        # 获取回单中所有表格坐标
        table_rects = [table.rect for table in pdf_profile.tables]
        # 根据表格坐标提取表格之间的间隔纵坐标
        ys = [(table_rects[index - 1][3], table_rects[index][1]) for index in range(1, len(table_rects))]
        # 将所有表格外的文本根据纵坐标进行分组
        all_interval_words = []
        for y in ys:
            interval_words = [word for word in pdf_profile.words if word.rect[1] > y[0] and word.rect[3] < y[1]]
            all_interval_words.append(interval_words)
        if not all_interval_words:
            if not len(pdf_profile.tables):
                return []
            elif len(pdf_profile.tables) > 1:
                raise ValueError("异常格式，无法处理")
            else:
                return [ReceiptProfile(pdf_profile.tables[0], pdf_profile.words)]
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
            split_ys.append(split_y)
        split_ys = [0] + split_ys + [999999]
        # 根据纵坐标分割回单
        receipt_profiles = []
        for index in range(1, len(split_ys)):
            receipt_profile = ReceiptProfile()
            for table in pdf_profile.tables:
                if table.rect[1] > split_ys[index - 1] and table.rect[3] < split_ys[index]:
                    assert receipt_profile.table is None, "异常格式，一个回单判断出来多个表格"
                    receipt_profile.table = table
            for word in pdf_profile.words:
                if word.rect[1] > split_ys[index - 1] and word.rect[3] < split_ys[index]:
                    receipt_profile.words.append(word)
            receipt_profiles.append(receipt_profile)
        return receipt_profiles
