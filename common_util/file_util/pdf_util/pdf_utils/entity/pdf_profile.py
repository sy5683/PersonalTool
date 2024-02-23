import typing

from .pdf_element import Table, Word


class PdfProfile:

    def __init__(self):
        self.tables: typing.List[Table] = []
        self.words: typing.List[Word] = []
