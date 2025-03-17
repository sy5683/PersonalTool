import subprocess
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

    @classmethod
    def open_file(cls, file_path: str):
        """打开文件"""
        try:
            subprocess.run(('xdg-open', file_path), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise FileExistsError(f"文件不存在: {file_path}")
