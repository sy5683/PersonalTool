import typing

from .pdf_element import Table, Word


class PdfProfile:
    """每页pdf中的对象"""

    def __init__(self):
        self.tables: typing.List[Table] = []
        self.words: typing.List[Word] = []
        self.image = None


class TableProfile:
    """每页pdf中可能有多个表格或者没有表格，这里以每个表格为一个单元将其进行分割"""

    def __init__(self, table: Table = None, words: typing.List[Word] = None):
        self.table: typing.Union[Table, None] = table
        self.words: typing.List[Word] = words if words else []
        self.image = None
        self.__rect = None

    def get_rect(self) -> typing.Tuple[float, float, float, float]:
        if self.__rect is None:
            pdf_elements = [self.table] + self.words
            if pdf_elements == [None]:
                return 0, 0, 0, 0
            x1 = min([pdf_element.rect[0] for pdf_element in pdf_elements if pdf_element])
            y1 = min([pdf_element.rect[1] for pdf_element in pdf_elements if pdf_element])
            x2 = max([pdf_element.rect[2] for pdf_element in pdf_elements if pdf_element])
            y2 = max([pdf_element.rect[3] for pdf_element in pdf_elements if pdf_element])
            self.__rect = (x1, y1, x2, y2)
        return self.__rect
