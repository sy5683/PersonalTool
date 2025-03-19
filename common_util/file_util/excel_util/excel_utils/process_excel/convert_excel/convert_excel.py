import abc
import logging
import os
import typing
from pathlib import Path


class ConvertExcel:

    @classmethod
    @abc.abstractmethod
    def re_save_excel(cls, excel_path: str):
        """重新保存excel"""
        logging.info(f"重新保存excel: {excel_path}")
        cls.__get_subclass().re_save_excel(excel_path)

    @classmethod
    @abc.abstractmethod
    def xls_to_xlsx(cls, excel_path: str, save_path: typing.Union[Path, str]) -> str:
        """xls文件转换为xlsx文件"""
        logging.info(f"开始将xls文件转换为xlsx: {excel_path}")
        return cls.__get_subclass().xls_to_xlsx(excel_path, save_path)

    @classmethod
    @abc.abstractmethod
    def excel_to_images(cls, excel_path: str, save_path: typing.Union[Path, str]) -> typing.List[str]:
        """excel转图片"""
        logging.info(f"开始将Excel文件转换为图片: {excel_path}")
        return cls.__get_subclass().excel_to_images(excel_path, save_path)

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .convert_excel_windows import ConvertExcelWindows
            return ConvertExcelWindows
        elif os.name == "posix":
            from .convert_excel_linux import ConvertExcelLinux
            return ConvertExcelLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
