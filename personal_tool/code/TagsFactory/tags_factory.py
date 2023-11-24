import re
from enum import Enum

from tags_factory.feature.pinyin_feature import PinyinFeature


class Operations(Enum):
    to_class = {'name': "类实例", 'format': """\t\tself.{object_name} = None  # {tag}"""}
    to_dict = {'name': "字典", 'format': """'{object_name}': ""  # {tag}"""}
    to_factory = {'name': "工厂方法", 'format': """\t\t\tentity.{object_name} = data.get("{tag}")"""}
    to_tag_width_tuples = {'name': "表头行宽映射", 'format': """({tag}, 16),"""}

    def to_format(self) -> str:
        return self.value['format']


class TagsFactory:
    """excel表头转换工厂"""

    def __init__(self, tags: str):
        self.tags = tags
        self.gong_si_ming_cheng = None  # 公司名称

    def main(self, operation, **kwargs):
        for tag in self.tags.split("\t"):
            kwargs['tag'] = tag
            temp_tag = re.sub(r"\((.*?)\)|（(.*?)）|-", "", tag)  # 去除表头中的特殊字符
            kwargs['object_name'] = PinyinFeature.chinese_to_object_name(temp_tag)
            print(operation.to_format().format(**kwargs))


if __name__ == '__main__':
    tags_factory = TagsFactory("""""")
    tags_factory.main(Operations.to_class)
