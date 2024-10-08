import abc
import re
import typing


class PdfElement(metaclass=abc.ABCMeta):

    def __init__(self, rect: typing.Tuple[float, float, float, float]):
        self.rect = rect

    def get_center(self) -> typing.Tuple[float, float]:
        return (self.rect[0] + self.rect[2]) / 2, (self.rect[1] + self.rect[3]) / 2

    def update_rect(self, rect: typing.Tuple[float, float, float, float]):
        self.rect = rect


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

    def get_value(self, interval: str = '') -> str:
        value = interval.join([word.text for word in self.words])
        return value if interval else re.sub(r"\s+", "", value)


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
        raise IndexError(f"未找到指定坐标的表格单元格: {row, col}")

    def get_cell_relative(self, pattern: str, relative: int = 1) -> Cell:
        """
        根据相对坐标获取单元格的值，主要是用于上侧单元格行数不确定的情况
        只用于左侧单元格是键，右侧单元格是值的情况，relative用于右侧偏移单元格数量
        """
        for row in range(self.max_rows):
            row_cells = self.get_row_cells(row)
            for col, row_cell in enumerate(row_cells):
                if re.search(pattern, row_cell.get_value()):
                    return row_cells[col + relative]
        raise ValueError(f"未找到指定值的单元格: {pattern}")

    def get_col_cells(self, col: int) -> typing.List[Cell]:
        return [cell for cell in self.cells if cell.col == col]

    def get_col_values(self, col: int) -> typing.List[str]:
        return [cell.get_value() for cell in self.get_col_cells(col)]

    def get_row_cells(self, row: int) -> typing.List[Cell]:
        return [cell for cell in self.cells if cell.row == row]

    def get_row_values(self, row: int) -> typing.List[str]:
        return [cell.get_value() for cell in self.get_row_cells(row)]
