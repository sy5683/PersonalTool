import importlib
import os
from pathlib import Path


class ImportUtil:

    @staticmethod
    def import_module(dir_path: Path):
        """导入指定路径文件"""
        if dir_path.stem == ".py":
            py_paths = [dir_path]
        else:
            py_paths = dir_path.rglob("*.py")

        for py_path in py_paths:
            py_parts = py_path.parts
            for i in range(len(py_parts), 1, -1):
                try:
                    module_name = ".".join(py_parts[i - 1:])
                    importlib.import_module(os.path.splitext(module_name)[0])  # 一定要记得去除导入路径的后缀
                    break
                except ModuleNotFoundError:
                    pass
