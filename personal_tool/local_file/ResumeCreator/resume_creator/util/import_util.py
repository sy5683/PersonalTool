import importlib
import re
from pathlib import Path
from types import ModuleType


class ImportUtil:

    @classmethod
    def import_modules(cls, module_path: Path):
        """导入指定路径下所有文件"""
        py_paths = [module_path] if module_path.suffix == ".py" else module_path.rglob("*.py")
        for py_path in py_paths:
            module_parts = py_path.parts
            for i in range(len(module_parts), 1, -1):
                try:
                    cls._import_module(".".join(module_parts[i - 1:]))
                except ModuleNotFoundError:
                    pass

    @staticmethod
    def _import_module(module_name: str) -> ModuleType:
        """导入"""
        # 一定要记得去除导入路径的后缀，否则会导入失败
        module_name = re.sub(r"\.py$", "", module_name)
        # 有__init__.py时需要导入其所在文件夹
        module_name = re.sub(r"\.__init__$", "", module_name)
        return importlib.import_module(module_name)
