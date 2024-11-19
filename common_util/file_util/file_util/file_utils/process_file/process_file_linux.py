import typing

from .process_file import ProcessFile


class ProcessFileLinux(ProcessFile):

    @classmethod
    def get_directory_path(cls) -> str:
        """获取文件夹路径"""
        raise Exception("Linux不支持tkinter")

    @classmethod
    def get_file_path(cls) -> str:
        """获取文件路径"""
        raise Exception("Linux不支持tkinter")

    @classmethod
    def get_file_paths(cls) -> typing.Literal[""] | typing.Tuple[str, ...]:
        """获取文件路径列表"""
        raise Exception("Linux不支持tkinter")

    @classmethod
    def get_root_paths(cls) -> typing.List[str]:
        """获取电脑根路径列表"""
        return ["/"]
