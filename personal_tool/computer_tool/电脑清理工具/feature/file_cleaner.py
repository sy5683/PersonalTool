import logging
import tempfile
import typing

from common_util.file_util.file_util.file_util import FileUtil


class FileCleaner:
    """文件清理工具"""

    @classmethod
    def clean_tempdir(cls):
        """清理临时文件夹"""
        cls._clean_dir(tempfile.gettempdir(), "临时文件夹")  # C:\Users\20727\AppData\Local\Temp

    @staticmethod
    def _clean_dir(dir_path: typing.Union[pathlib.Path, str], name: str = ''):
        """清理文件夹"""
        logging.info(f"清理{name.strip('文件夹')}文件夹: {dir_path}")
        for file_path in pathlib.Path(dir_path).glob("*"):
            FileUtil.delete_file(file_path)
