import tempfile
from pathlib import Path

from .process_file import ProcessFile


class ProcessTempFile:
    """处理临时文件"""
    _temp_dir_path = None

    @classmethod
    def get_temp_path(cls, file_name: str) -> Path:
        """获取临时文件路径"""
        if cls._temp_dir_path is None:
            cls._temp_dir_path = Path(tempfile.mkdtemp())
        temp_path = cls._temp_dir_path.joinpath(file_name)
        ProcessFile.make_dir(temp_path)
        return temp_path
