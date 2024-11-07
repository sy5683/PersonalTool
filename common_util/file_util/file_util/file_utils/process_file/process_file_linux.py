import typing

from .process_file import ProcessFile


class ProcessFileLinux(ProcessFile):

    @classmethod
    def get_root_paths(cls) -> typing.List[str]:
        """获取电脑根路径列表"""
        return ["\\"]
