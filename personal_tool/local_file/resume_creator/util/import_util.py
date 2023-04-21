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
            for i in range(1, len(py_parts)):
                try:
                    module_name = ".".join(py_parts[i:])
                    module_name = os.path.splitext(module_name)[0]  # 一定要记得去除导入路径的后缀，否则会导入失败
                    importlib.import_module(module_name)
                    break
                except ModuleNotFoundError:
                    pass
