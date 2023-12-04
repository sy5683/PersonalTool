import typing
from pathlib import Path

from common_core.base.util_base import UtilBase
from .file_utils.process_file import ProcessFile
from .file_utils.process_temp_file import ProcessTempFile


class FileUtil(UtilBase):

    @staticmethod
    def format_path(file_path: typing.Union[Path, str]) -> Path:
        """格式化路径"""
        return ProcessFile.format_path(Path(file_path))

    @staticmethod
    def get_directory_path() -> str:
        """获取文件夹路径"""
        return ProcessFile.get_directory_path()

    @staticmethod
    def get_file_path() -> str:
        """获取文件路径"""
        return ProcessFile.get_file_path()

    @staticmethod
    def get_file_paths() -> typing.Tuple[str]:
        """获取文件路径列表"""
        return ProcessFile.get_file_paths()

    @staticmethod
    def get_original_type(file_path: typing.Union[Path, str]) -> str:
        """获取文件原始类型"""
        return ProcessFile.get_original_type(str(file_path))

    @staticmethod
    def get_temp_path(file_name: str = '') -> Path:
        """获取临时文件路径"""
        return ProcessTempFile.get_temp_path(file_name)

    @staticmethod
    def make_dir(file_path: typing.Union[Path, str]):
        """新建文件夹"""
        ProcessFile.make_dir(Path(file_path))

    @staticmethod
    def wait_file_appear(file_path: typing.Union[Path, str], wait_seconds: int = 120) -> bool:
        """等待文件出现"""
        return ProcessFile.wait_file_appear(Path(file_path), wait_seconds)
