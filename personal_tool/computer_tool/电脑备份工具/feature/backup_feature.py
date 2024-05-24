import logging
import shutil
import typing
from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class BackupFeature:

    @classmethod
    def backup_file(cls, file_path: typing.Union[str, Path], save_name: str = ''):
        """备份文件"""
        backup_save_path = cls.get_backup_save_path(save_name)
        backup_save_path = backup_save_path.joinpath(Path(file_path).name)
        logging.info(f"备份文件: {backup_save_path}")
        shutil.copy(file_path, backup_save_path)

    @staticmethod
    def get_backup_save_path(file_name: str = '') -> Path:
        """获取备份保存路径"""
        backup_save_path = Path(__file__).parent.parent.joinpath(f"file\\备份文件\\{file_name}")
        FileUtil.make_dir(backup_save_path)
        return backup_save_path
