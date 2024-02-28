import typing

from .pdf_element import Table, Word


class PdfProfile:

    def __init__(self):
        self.tables: typing.List[Table] = []
        self.words: typing.List[Word] = []


class ReceiptProfile:

    def __init__(self, table: Table = None, words: typing.List[Word] = None):
        self.table: typing.Union[Table, None] = table
        self.words: typing.List[Word] = words if words else []
