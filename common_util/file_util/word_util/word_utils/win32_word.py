import logging
import os
import typing
from pathlib import Path

from win32com.client import constants, gencache


class Win32Word:

    @staticmethod
    def word_to_pdf(word_path: str, save_path: typing.Union[Path, str]) -> str:
        """word转pdf"""
        logging.info(f"开始将word文件转换为pdf: {word_path}")
        _path, suffix = os.path.splitext(word_path)
        assert suffix == ".docx", f"待转换word不为docx文件: {word_path}"
        save_path = f"{_path}.pdf" if save_path is None else str(save_path)
        app = gencache.EnsureDispatch('Word.Application')
        document = app.Documents.Open(word_path, ReadOnly=True)
        document.ExportAsFixedFormat(save_path, constants.wdExportFormatPDF, Item=constants.wdExportDocumentWithMarkup,
                                     CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        document.Close()
        app.Quit(constants.wdDoNotSaveChanges)
        logging.info(f"成功将word文件转换为pdf: {word_path}")
        return save_path
