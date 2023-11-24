import re
from pathlib import Path

import excel2img
import xlrd

from .feature.file_feature import FileFeature


class ExcelConverter:

    @staticmethod
    def excel_to_images():
        """excel转图片"""
        file_paths = FileFeature.get_file_paths()
        assert re.match(r"\.xlsx", FileFeature.get_suffix()), "选择的文件无法进行excel转图片操作"
        for file_path in file_paths:
            file_name = Path(file_path).stem
            # 获取sheet
            wb = xlrd.open_workbook(file_path)
            for index, sheet_name in enumerate(wb.sheet_names()):
                image_path = FileFeature.get_save_path(f"{file_name}_{sheet_name}.png")
                excel2img.export_img(file_path, image_path, page=index + 1)
