import typing

from .pdf_element import Table, Word


class PdfProfile:
    """每页pdf中的对象"""

    def __init__(self):
        self.tables: typing.List[Table] = []
        self.words: typing.List[Word] = []


class ReceiptProfile:

    def __init__(self, table: Table = None, words: typing.List[Word] = None):
        self.table: typing.Union[Table, None] = table
        self.words: typing.List[Word] = words if words else []


class TableProfile:
    """每页pdf中可能有多个表格或者没有表格，这里以每个表格为一个单元将其进行分割"""

    def __init__(self, table: Table = None, words: typing.List[Word] = None):
        self.table: typing.Union[Table, None] = table
        self.words: typing.List[Word] = words if words else []
