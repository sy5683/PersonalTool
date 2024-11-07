import os
import typing

from .process_file import ProcessFile


class ProcessFileWindows(ProcessFile):

    @classmethod
    def get_root_paths(cls) -> typing.List[str]:
        """获取电脑根路径列表"""
        return [root_dir for root_dir in [f"{chr(65 + index)}:\\" for index in range(26)] if os.path.exists(root_dir)]
