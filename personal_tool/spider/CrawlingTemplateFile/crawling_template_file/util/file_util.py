import re
import tempfile
import uuid
from pathlib import Path


class FileUtil:
    _temp_dir_path = None

    @classmethod
    def get_temp_path(cls, file_name: str = '') -> Path:
        """获取临时文件路径"""
        if cls._temp_dir_path is None:
            cls._temp_dir_path = Path(tempfile.mkdtemp())
        temp_path = cls._temp_dir_path.joinpath(file_name)
        temp_dir_path = temp_path.parent if temp_path.suffix else temp_path
        temp_dir_path.mkdir(exist_ok=True, parents=True)
        return temp_path

    @classmethod
    def get_temp_file_path(cls, suffix: str = 'tmp') -> Path:
        suffix = suffix if re.search(r"^\.", suffix) else f".{suffix}"
        file_name = f"temp_file_{uuid.uuid4()}{suffix}"
        return cls.get_temp_path(file_name)
