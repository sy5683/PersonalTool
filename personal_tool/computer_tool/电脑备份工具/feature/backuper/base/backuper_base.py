import abc
import logging
import os
import shutil
import typing
from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class BackuperBase(abc.ABCMeta):

    @classmethod
    def backup_file(cls, file_path: typing.Union[str, Path], save_name: str = ''):
        """备份文件"""
        backup_save_path = cls._get_backup_save_path(save_name)
        FileUtil.make_dir(backup_save_path)
        backup_save_path = backup_save_path.joinpath(Path(file_path).name)
        logging.info(f"备份文件: {backup_save_path}")
        shutil.copy(file_path, backup_save_path)

    @classmethod
    def update_file(cls, file_path: typing.Union[str, Path], save_name: str = ''):
        """更新文件"""
        save_path = os.path.join(save_name, Path(file_path).name)
        backup_save_path = cls._get_backup_save_path(save_path)
        if not backup_save_path.exists():
            raise FileNotFoundError(f"本地没有目标对应的备份文件，无法更新: {save_path}")
        logging.info(f"更新文件: {backup_save_path}")
        shutil.copy(backup_save_path, file_path)

    @staticmethod
    def _get_backup_save_path(*file_names: str) -> Path:
        """获取备份保存路径"""
        return Path(__file__).parent.parent.parent.parent.joinpath("file", "备份文件", *file_names)
