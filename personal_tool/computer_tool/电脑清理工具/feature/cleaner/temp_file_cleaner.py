import logging
import tempfile
from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class TempFileCleaner:

    @staticmethod
    def clean_tempdir():
        """清理临时文件夹"""
        tempdir_path = tempfile.gettempdir()
        logging.info(f"清理临时文件夹: {tempdir_path}")
        for file_path in Path(tempdir_path).glob("*"):
            FileUtil.delete_file(file_path)
