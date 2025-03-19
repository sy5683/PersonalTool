import logging
import os
import typing
from pathlib import Path

from win32com.client import constants, gencache

from .convert_word import ConvertWord


class ConvertWordWindows(ConvertWord):

    @classmethod
    def word_to_pdf(cls, word_path: str, save_path: typing.Union[Path, str]) -> str:
        """word转pdf"""
        save_path = f"{os.path.splitext(word_path)[0]}.pdf" if save_path is None else str(save_path)
        assert not os.path.exists(save_path), f"文件已存在，无法转换: {save_path}"
        app = gencache.EnsureDispatch('Word.Application')
        document = app.Documents.Open(word_path, ReadOnly=True)
        document.ExportAsFixedFormat(save_path, constants.wdExportFormatPDF, Item=constants.wdExportDocumentWithMarkup,
                                     CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        document.Close()
        app.Quit(constants.wdDoNotSaveChanges)
        logging.info(f"成功将word文件转换为pdf: {word_path}")
        return save_path
