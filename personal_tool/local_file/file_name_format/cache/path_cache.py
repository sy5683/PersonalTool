import tkinter
from pathlib import Path
from tkinter import filedialog


class PathCache:
    _directory_path = None

    @classmethod
    def get_directory_path(cls) -> Path:
        if cls._directory_path is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._directory_path = Path(filedialog.askdirectory())
        return cls._directory_path
