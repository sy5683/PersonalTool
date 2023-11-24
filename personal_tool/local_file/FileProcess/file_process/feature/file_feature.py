import tkinter
import typing
from tkinter import filedialog


class FileFeature:
    _file_paths = None

    @classmethod
    def get_file_paths(cls) -> typing.List[str]:
        if cls._file_paths is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._file_paths = list(filedialog.askopenfilenames())
        return cls._file_paths
