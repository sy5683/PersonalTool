import re
import typing


class TagFeature:

    @staticmethod
    def split_tags(tags: typing.Union[typing.List[str], str]) -> typing.List[str]:
        if isinstance(tags, list):
            return [str(tag) for tag in tags]
        elif isinstance(tags, str):
            return re.split(r"\s+", str(tags))
        raise Exception(f"未知的参数类型【{type(tags)}】: {tags}")
