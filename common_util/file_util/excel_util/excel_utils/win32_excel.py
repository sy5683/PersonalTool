import logging
import os
import typing
from pathlib import Path

import excel2img
import xlrd
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
    def xls_to_xlsx(excel_path: str, save_path: typing.Union[Path, str]) -> str:
        """xls文件转换为xlsx文件"""
        logging.info(f"开始将xls文件转换为xlsx: {excel_path}")
        _path, suffix = os.path.splitext(excel_path)
        assert suffix == ".xls", f"待转换excel不为xls文件: {excel_path}"
        save_path = f"{_path}.xlsx" if save_path is None else str(save_path)
        assert not os.path.exists(save_path), f"文件已存在，无法转换: {save_path}"
        app = Dispatch("Excel.Application")
        workbook = app.Workbooks.Open(excel_path)
        workbook.SaveAs(save_path, FileFormat=51)  # xlsx格式的FileFormat=51
        workbook.Close()
        app.Application.Quit()
        logging.info(f"成功将xls文件转换为xlsx: {save_path}")
        return save_path

    @staticmethod
    def excel_to_images(excel_path: str, save_path: typing.Union[Path, str]) -> typing.List[str]:
        """excel转图片"""
        logging.info(f"开始将Excel文件转换为图片: {excel_path}")
        save_path = os.path.splitext(excel_path)[0] if save_path is None else str(save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        image_paths = []
        wb = xlrd.open_workbook(excel_path)
        for index, sheet_name in enumerate(wb.sheet_names()):
            image_path = os.path.join(save_path, f"{sheet_name}.png")
            excel2img.export_img(excel_path, image_path, page=index + 1)
            image_paths.append(image_path)
        logging.info(f"成功将Excel文件转换为图片: {save_path}")
        return image_paths
