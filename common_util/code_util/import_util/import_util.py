import typing
from pathlib import Path
from types import ModuleType

from common_core.base.util_base import UtilBase
from .import_utils.import_path import ImportPath


class ImportUtil(UtilBase):

    @staticmethod
    def import_module(module_path: typing.Union[Path, str]) -> ModuleType:
        """导入路径下文件"""
        return ImportPath.import_module(Path(module_path))

    @staticmethod
    def import_modules(module_path: typing.Union[Path, str]):
        """导入指定路径下所有文件"""
        ImportPath.import_modules(Path(module_path))
