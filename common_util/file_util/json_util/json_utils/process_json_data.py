import typing


class ProcessJsonData:

    @staticmethod
    def sort_json(json_data: typing.Union[dict, typing.List[dict]]) -> typing.Union[dict, typing.List[dict]]:
        """json排序"""
        if isinstance(json_data, dict):
            json_data = {key: json_data[key] for key in sorted(json_data)}
        return json_data
