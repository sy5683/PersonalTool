import pathlib
import typing
from types import ModuleType

from .import_utils.import_path import ImportPath


class ImportUtil:

    @staticmethod
    def import_module(module_path: typing.Union[pathlib.Path, str]) -> ModuleType:
        """导入路径下文件"""
        return ImportPath.import_module(pathlib.Path(module_path))

    @staticmethod
    def import_modules(module_path: typing.Union[pathlib.Path, str]):
        """导入指定路径下所有文件"""
        ImportPath.import_modules(pathlib.Path(module_path))
