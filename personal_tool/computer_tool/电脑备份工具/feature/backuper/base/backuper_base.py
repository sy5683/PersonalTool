import abc
import logging
import os
import pathlib
import shutil
import typing

from common_util.file_util.file_util.file_util import FileUtil


class BackuperBase(abc.ABCMeta):

    @classmethod
    def backup_file(cls, file_path: typing.Union[str, pathlib.Path], save_name: str = ''):
        """备份文件"""
        backup_save_path = cls._get_backup_save_path(save_name)
        FileUtil.make_dir(backup_save_path)
        backup_save_path = backup_save_path.joinpath(pathlib.Path(file_path).name)
        logging.info(f"备份文件: {backup_save_path}")
        shutil.copy(file_path, backup_save_path)

    @classmethod
    def update_file(cls, file_path: typing.Union[str, pathlib.Path], save_name: str = ''):
        """更新文件"""
        save_path = os.path.join(save_name, pathlib.Path(file_path).name)
        backup_save_path = cls._get_backup_save_path(save_path)
        if not backup_save_path.exists():
            raise FileNotFoundError(f"本地没有目标对应的备份文件，无法更新: {save_path}")
        logging.info(f"更新文件: {backup_save_path}")
        shutil.copy(backup_save_path, file_path)

    @staticmethod
    def _get_backup_save_path(*file_names: str) -> pathlib.Path:
        """获取备份保存路径"""
        return pathlib.Path(__file__).parent.parent.parent.parent.joinpath("file", "备份文件", *file_names)
