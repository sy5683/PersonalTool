import logging
import tempfile
from pathlib import Path

from ..clean_feature import CleanFeature


class TempFileCleaner:

    @staticmethod
    def clean_tempdir():
        """清理临时文件夹"""
        tempdir_path = tempfile.gettempdir()
        logging.info(f"清理临时文件夹: {tempdir_path}")
        for file_path in Path(tempdir_path).glob("*"):
            CleanFeature.delete_file(file_path)
