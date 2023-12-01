import os
import re
import typing
from pathlib import Path

import natsort


class FileFeature:

    @staticmethod
    def get_file_paths(directory_path: Path) -> typing.List[Path]:
        """获取文件路径列表"""
        # 获取文件路径列表，使用os_sorted将其根据windows顺序排序
        return natsort.os_sorted(list(directory_path.glob("*.*")))

    @staticmethod
    def file_rename(path: Path, new_name: str = None) -> Path:
        """重命名"""
        if new_name is None:
            # 重新生成文件路径，防止其父辈文件夹中名称有temp开头的文件夹被误重命名
            new_path = path.parent.joinpath(re.sub(r"^temp_", "", path.stem) + path.suffix)
        else:
            # 因为会有文件名已存在的情况，因此这里生成新文件名时需要添加temp防止重复
            new_path = path.parent.joinpath(f"temp_{new_name}")
        if path != new_path:
            os.rename(path, new_path)
        return new_path
