import typing

from .win32_visual import Win32Visual


class Win32VisualLinux(Win32Visual):

    @classmethod
    def close_handle(cls, class_name: str, title: str):
        """关闭窗口"""
        raise FileExistsError("暂不支持该功能")

    @classmethod
    def show_window(cls, handle: int, need_admin_right: bool):
        """显示窗口"""
        raise FileExistsError("暂不支持该功能")

    @classmethod
    def upload(cls, file_path: str, wait_seconds: int):
        """上传文件"""
        raise FileExistsError("暂不支持该功能")

    @classmethod
    def _find_handles(cls, class_name: str, title: str) -> typing.List[int]:
        """查找窗口句柄列表"""
        raise FileExistsError("暂不支持该功能")
