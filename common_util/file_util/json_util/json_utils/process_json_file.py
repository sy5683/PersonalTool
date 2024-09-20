import json
import typing

from .process_json_data import ProcessJsonData


class ProcessJsonFile:
    encoding_type = "UTF-8"

    @classmethod
    def read_json(cls, json_path: str) -> typing.Union[dict, list]:
        """读取json文件"""
        with open(json_path, "r", encoding=cls.encoding_type) as file:
            return json.load(file)

    @classmethod
    def write_json(cls, json_path: str, json_data: typing.Union[dict, typing.List[dict]], sort: bool):
        """写入json文件"""
        if sort:
            json_data = ProcessJsonData.sort_json(json_data)
        with open(json_path, "w", encoding=cls.encoding_type) as file:
            file.write(json.dumps(json_data, ensure_ascii=False, indent=2))
