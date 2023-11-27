import os.path

from win32com.client import Dispatch


class Win32Excel:

    @staticmethod
    def re_save_excel(excel_path: str):
        """
        重新保存excel
        因为使用openpyxl生成的excel，如果不手动打开并保存，其中的公式是未进行计算的，如果再次使用openpyxl进行读取，是取不到结果的
        因此需要使用win32重新将其打开并保存一次
        """
        app = Dispatch("Excel.Application")
        app.Visible = False
        workbook = app.Workbooks.Open(excel_path)
        workbook.Save()
        workbook.Close()
        app.Application.Quit()

    @staticmethod
    def xls_to_xlsx(excel_path: str) -> str:
        """xls文件转换为xlsx文件"""
        _path, suffix = os.path.splitext(excel_path)
        assert suffix == ".xls", "待转换excel不为xls文件"
        app = Dispatch("Excel.Application")
        workbook = app.Workbooks.Open(excel_path)
        workbook.Save()
        new_excel_path = f"{_path}.xlsx"
        # 如果新excel有重命文件，win32则会弹窗提示是否覆盖
        if os.path.exists(new_excel_path):
            os.remove(new_excel_path)
        workbook.SaveAs(new_excel_path, FileFormat=51)  # xlsx格式的FileFormat=51
        workbook.Close()
        app.Application.Quit()
        return new_excel_path
