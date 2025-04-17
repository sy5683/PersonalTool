import pathlib
import typing

from .json_utils.process_json_data import ProcessJsonData
from .json_utils.process_json_file import ProcessJsonFile


class JsonUtil:

    @staticmethod
    def read_json(json_path: typing.Union[pathlib.Path, str]) -> typing.Union[dict, list]:
        """读取json文件"""
        return ProcessJsonFile.read_json(str(json_path))

    @staticmethod
    def sort_json(json_data: typing.Union[dict, typing.List[dict]]) -> typing.Union[dict, typing.List[dict]]:
        """json排序"""
        return ProcessJsonData.sort_json(json_data)

    @staticmethod
    def write_json(json_path: typing.Union[pathlib.Path, str], json_data: typing.Union[dict, typing.List[dict]],
                   sort: bool = False):
        """写入json文件"""
        ProcessJsonFile.write_json(str(json_path), json_data, sort)
