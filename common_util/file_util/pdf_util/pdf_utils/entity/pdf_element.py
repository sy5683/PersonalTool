import abc
import typing


class PdfElement(metaclass=abc.ABCMeta):

    def __init__(self, rect: typing.Tuple[float, float, float, float]):
        self.rect = rect

    def get_center(self) -> typing.Tuple[float, float]:
        return (self.rect[0] + self.rect[2]) // 2, (self.rect[1] + self.rect[3]) // 2


class Word(PdfElement):

    def __init__(self, rect: typing.Tuple[float, float, float, float], text: str):
        super().__init__(rect)
        self.text = text


class Cell(PdfElement):

    def __init__(self, rect: typing.Tuple[float, float, float, float]):
        super().__init__(rect)
        self.words: typing.List[Word] = []
        self.row = None
        self.col = None

    def get_value(self) -> str:
        return "".join([word.text for word in self.words])


class Table(PdfElement):

    def __init__(self, rect: typing.Tuple[float, float, float, float]):
        super().__init__(rect)
        self.cells: typing.List[Cell] = []
        self.max_cols = None
        self.max_rows = None

    def get_cell(self, row: int, col: int) -> Cell:
        for cell in self.cells:
            if col != cell.col:
                continue
            if row != cell.row:
                continue
            return cell

    def get_col_cells(self, col: int) -> typing.List[Cell]:
        return [cell for cell in self.cells if cell.col == col]

    def get_col_values(self, col: int) -> typing.List[str]:
        return [cell.get_value() for cell in self.get_col_cells(col)]

    def get_row_cells(self, row: int) -> typing.List[Cell]:
        return [cell for cell in self.cells if cell.row == row]

    def get_row_values(self, row: int) -> typing.List[str]:
        return [cell.get_value() for cell in self.get_row_cells(row)]
