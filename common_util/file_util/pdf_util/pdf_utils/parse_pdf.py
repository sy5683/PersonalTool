import copy
import typing

import cv2
import fitz
import numpy

from .entity.pdf_element import Cell, Table, Word
from .entity.pdf_profile import PdfProfile


class ParsePdf:
    """解析pdf"""

    @classmethod
    def get_pdf_profiles(cls, pdf_path: str, threshold_x: int) -> typing.List[PdfProfile]:
        """获取pdf内容"""
        pdf_profiles = []
        with fitz.open(pdf_path) as pdf:
            for index in range(pdf.page_count):
                pdf_profile = PdfProfile()
                pdf_page = pdf[index]
                # 1.1) 获取pdf文字
                words = cls._get_words(pdf_page)
                # 1.2) 获取表格图像
                table_image = cls._get_table_image(pdf_page)
                # 1.3) 获取表格列表
                tables = cls._get_tables(table_image)
                # 2.1) 获取表格单元格列表
                cells = cls._get_table_cells(table_image, words)
                # 2.2) 将单元格合并至表格中
                cls._group_table_cells(tables, cells)
                pdf_profile.tables += tables
                # 3.1) 合并相近文字
                words = cls.__merge_words(words, threshold_x)
                # 3.2) 过滤表格中的文字
                pdf_profile.words += cls._filter_word_in_table(tables, words)
                pdf_profiles.append(pdf_profile)
        return pdf_profiles

    @classmethod
    def get_pdf_tables(cls, pdf_path: str) -> typing.List[Table]:
        """获取pdf中的表格"""
        pdf_tables = []
        # 因为表格是根据边框对数据进行分类合并的，因此无需考虑合并文字的操作，这个阈值随便写一个值就行
        for pdf_profile in cls.get_pdf_profiles(pdf_path, 1):
            pdf_tables += pdf_profile.tables
        return pdf_tables

    @classmethod
    def get_pdf_words(cls, pdf_path: str, threshold_x: int) -> typing.List[Word]:
        """获取pdf中的文字"""
        pdf_words = []
        for pdf_profile in cls.get_pdf_profiles(pdf_path, threshold_x):
            pdf_words += pdf_profile.words
        return pdf_words

    @classmethod
    def _filter_word_in_table(cls, tables: typing.List[Table], words: typing.List[Word]) -> typing.List[Word]:
        """过滤在表格中的文字"""

        def __check_word_in_tables(w: Word):
            for table in tables:
                if cls.__check_inside(w.get_center(), table.rect):
                    return True
            return False

        filter_words = []
        for word in words:
            if not __check_word_in_tables(word):
                filter_words.append(word)
        return filter_words

    @classmethod
    def _get_table_cells(cls, table_image: numpy.ndarray, words: typing.List[Word]):
        """根据轮廓，获取表格单元格列表"""
        # 查找相应的轮廓，得到每个表格cell的矩形框
        cells = []
        contours, hierarchy = cv2.findContours(table_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours[::-1]:
            r = cv2.boundingRect(contour)
            cell = Cell((r[0], r[1], r[0] + r[2], r[1] + r[3]))
            for word in words:
                if cls.__check_inside(word.get_center(), cell.rect):
                    cell.words.append(word)
            cells.append(cell)
        # 根据左上角坐标排序，从上至下，从左至右
        return cls.__sort_pdf_element(cells)

    @classmethod
    def _get_table_image(cls, page: fitz.Page) -> numpy.ndarray:
        """获取表格图像"""
        # 生成一个与pdf页面等大的图片对象
        pix_map = page.get_pixmap(matrix=fitz.Matrix(1, 1))
        image = numpy.zeros([pix_map.h, pix_map.w], dtype=numpy.uint8) + 255
        # 绘制pdf的线条
        for draw in page.get_drawings():
            color = list(draw.get("color") or [])
            fill = list(draw.get("fill") or [])
            if (color == [1.0, 1.0, 1.0] or color == [1.0]) and not fill:
                continue
            if (fill == [1.0, 1.0, 1.0] or fill == [1.0]) and not color:
                continue
            if color == [1.0, 1.0, 1.0] and fill == [1.0]:
                continue
            for items in draw['items']:
                if 'l' == items[0]:
                    p1, p2 = cls.__to_int(*items[1]), cls.__to_int(*items[2])
                    image = cv2.line(image, (p1[0], p1[1]), (p2[0], p2[1]), (0, 0, 0))
                elif 're' == items[0]:
                    p = cls.__to_int(*items[1])
                    image = cv2.rectangle(image, (p[0], p[1]), (p[2], p[3]), (0, 0, 0))
                elif 'c' == items[0]:
                    print('c', items)  # TODO
                else:
                    print(items)  # TODO
        # 使用漫水填充算法，将周围变为黑色，这样可以去掉单独的线条
        cv2.floodFill(image, None, (1, 1), (0, 0, 0), flags=cv2.FLOODFILL_FIXED_RANGE)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
        return image

    @classmethod
    def _get_tables(cls, table_image: numpy.ndarray) -> typing.List[Table]:
        """根据轮廓，获取表格列表"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morp = cv2.morphologyEx(table_image, cv2.MORPH_CLOSE, kernel, iterations=3)
        # 查找相应的轮廓，得到每个表格的矩形框
        contours, hierarchy = cv2.findContours(morp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tables = []
        for contour in contours:
            rect = cv2.boundingRect(contour)
            tables.append(Table((rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])))
        return cls.__sort_pdf_element(tables)

    @staticmethod
    def _get_words(pdf_page: fitz.Page) -> typing.List[Word]:
        """根据坐标，获取pdf文字"""
        pdf_words = pdf_page.get_text_words()
        # 将文字转为列表
        words = []
        for pdf_word in pdf_words:
            # 有些文字旋转过，需要旋转回来
            p1 = fitz.Point(pdf_word[0], pdf_word[1]) * pdf_page.rotation_matrix
            p2 = fitz.Point(pdf_word[2], pdf_word[3]) * pdf_page.rotation_matrix
            # 旋转后矩形点位置发生改变，需要还原
            p3 = min(p1[0], p2[0]), min(p1[1], p2[1])  # 左上
            p4 = max(p1[0], p2[0]), max(p1[1], p2[1])  # 右下
            words.append(Word((p3[0], p3[1], p4[0], p4[1]), pdf_word[4]))
        # 根据左上角坐标排序，从上至下，从左至右
        return sorted(words, key=lambda x: (x.rect[1], x.rect[0]))

    @classmethod
    def _group_table_cells(cls, tables: typing.List[Table], cells: typing.List[Cell]):
        """分组表格单元格"""
        for table in tables:
            for cell in cells:
                if cls.__check_inside(cell.get_center(), table.rect):
                    table.cells.append(cell)
            # 当所有单元格分组后，根据所有单元格坐标绘制表格中的行高定位
            xs = sorted(set([cell.rect[0] for cell in table.cells]))
            ys = sorted(set([cell.rect[1] for cell in table.cells]))
            table.max_cols = len(xs)
            table.max_rows = len(ys)
            for cell in cells:
                if cls.__check_inside(cell.get_center(), table.rect):
                    cell.col = xs.index(cell.rect[0])
                    cell.row = ys.index(cell.rect[1])

    @staticmethod
    def __check_inside(point: typing.Tuple[float, float], rect: typing.Tuple[float, float, float, float]):
        """判断点是否在框内"""
        return rect[0] <= point[0] <= rect[2] and rect[1] <= point[1] <= rect[3]

    @staticmethod
    def __merge_words(words: typing.List[Word], threshold_x: int) -> typing.List[Word]:
        """合并相近的文字"""
        new_words = []
        for index, word in enumerate(copy.deepcopy(words)):
            # 第一条数据
            if not index:
                new_words.append(word)
                continue
            # 单个词语的坐标信息
            x1, y1, x2, y2 = word.rect
            last_word = new_words[-1]
            x_min, y_min, x_max, y_max = last_word.rect
            # 根据坐标判断是否需要合并
            if y1 < y_max and x1 - x_max < threshold_x:
                x_min, y_min, x_max, y_max = min(x_min, x1), min(y_min, y1), max(x_max, x2), max(y_max, y2)
                last_word.rect = (x_min, y_min, x_max, y_max)
                last_word.text += word.text
            else:  # 新的一行
                new_words.append(word)
        return new_words

    @staticmethod
    def __sort_pdf_element(pdf_elements: typing.List[typing.Union[Cell, Word, Table]]):
        """根据左上角坐标排序，从上至下，从左至右"""
        return sorted(pdf_elements, key=lambda x: (x.rect[1], x.rect[0]))

    @staticmethod
    def __to_int(*kwargs) -> typing.List[int]:
        return [int(each) for each in kwargs]
