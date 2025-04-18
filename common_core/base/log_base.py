import abc
import pathlib
import sys

from ..tool.log_tool.log_tool import LogTool


class LogBase(metaclass=abc.ABCMeta):
    # 日志输出到控制台
    LogTool.add_console_handler()

    def __init__(self):
        # 日志保存至本地文件
        log_path = self.get_subclass_path(f"file/logs/{self.get_subclass_path().parent.stem}.log")
        LogTool.add_file_handler(log_path)

    def get_subclass_path(self, file_name: str = None) -> pathlib.Path:
        """
        获取子类文件路径
        传入file_name时，会生成子类同级的路径
        """
        file_path = pathlib.Path(sys.modules[self.__module__].__file__)
        if file_name:
            file_path = file_path.parent.joinpath(file_name)
            dir_path = file_path.parent if file_path.suffix else file_path
            dir_path.mkdir(exist_ok=True, parents=True)
        return file_path
