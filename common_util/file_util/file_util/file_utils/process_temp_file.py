import pathlib
import tempfile

from .process_file.process_file import ProcessFile


class ProcessTempFile:
    __temp_dir_path = None

    @classmethod
    def get_temp_path(cls, file_name: str) -> pathlib.Path:
        """获取临时文件路径"""
        if cls.__temp_dir_path is None:
            cls.__temp_dir_path = pathlib.Path(tempfile.mkdtemp())
        temp_path = cls.__temp_dir_path.joinpath(file_name)
        ProcessFile.make_dir(temp_path)
        return temp_path
