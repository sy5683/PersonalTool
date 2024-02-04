import logging
import os
import shutil
import tempfile
import typing
from pathlib import Path


class CleanFeature:

    @classmethod
    def clean_tempdir(cls):
        """清理临时文件夹"""
        tempdir_path = tempfile.gettempdir()
        logging.info(f"清理临时文件夹: {tempdir_path}")
        for file_path in Path(tempdir_path).glob("*"):
            cls._delete_file(file_path)

    @staticmethod
    def _delete_file(file_path: typing.Union[Path, str]):
        """删除文件"""
        try:
            if Path(file_path).is_dir():
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        except PermissionError:
            pass
