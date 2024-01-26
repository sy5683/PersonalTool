import os
import shutil
import typing
from pathlib import Path


class CleanFeature:

    @classmethod
    def clean_dir(cls, dir_path: typing.Union[Path, str]):
        """清空文件夹"""
        for file_path in Path(dir_path).glob("*"):
            cls.delete_file(file_path)
        print(f"清空文件夹: {dir_path}")

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
