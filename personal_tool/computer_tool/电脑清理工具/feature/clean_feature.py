import os
import shutil
import typing
from pathlib import Path


class CleanFeature:

    @staticmethod
    def delete_file(file_path: typing.Union[Path, str]):
        """删除文件"""
        try:
            if Path(file_path).is_dir():
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        except PermissionError:
            pass
