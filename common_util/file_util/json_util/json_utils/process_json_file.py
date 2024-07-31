import json
import typing

from .process_json_data import ProcessJsonData


class ProcessJsonFile:

    @staticmethod
    def write_json(json_path: str, json_data: typing.Union[dict, typing.List[dict]], sort: bool):
        """写入json文件"""
        if sort:
            json_data = ProcessJsonData.sort_json(json_data)
        with open(json_path, "w", encoding='UTF-8') as file:
            file.write(json.dumps(json_data, ensure_ascii=False, indent=2))
