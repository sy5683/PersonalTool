import re
import typing
from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.data_util.textual_util.textual_util import TextualUtil
from feature.tag_feature import TagFeature


class Operations(Enum):
    to_class = {'name': "类实例", 'format': """\t\tself.{object_name} = None  # {tag}"""}
    to_dict = {'name': "字典", 'format': """'{object_name}': ""  # {tag}"""}
    to_factory = {'name': "工厂方法", 'format': """\t\t\tself.{object_name} = data.get("{tag}")"""}
    to_result_list = {'name': "对象名称", 'format': "self.{object_name},"}
    to_tag_width_tuples = {'name': "表头行宽映射", 'format': """({tag}, 16),"""}

    def to_name(self) -> str:
        return self.value['name']

    def to_format(self) -> str:
        return self.value['format']


class TagsConverter(ToolBase):

    def __init__(self, operation: Operations):
        super().__init__()
        self.show_str = operation.to_format()

    def main(self, tags: typing.Union[typing.List[str], str]):
        for tag in TagFeature.split_tags(tags):
            temp_tag = re.sub(r"[()（）\-]|^_", "", tag)  # 去除表头中的特殊字符
            object_name = TextualUtil.chinese_to_object_name(temp_tag)
            print(self.show_str.format(tag=tag, object_name=object_name))


if __name__ == '__main__':
    tags_converter = TagsConverter(Operations.to_class)
    tags_converter.main("""测试123 _拼音(正则)""")
