import typing
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from common_util.data_util.textual_util.textual_util import TextualUtil
from .entity.character import Character


class CharacterFeature:
    _characters = None

    @classmethod
    def show_characters(cls):
        cls._show_characters("攻击")
        cls._show_characters("移动速度")
        cls._show_characters("工作速度")

    @classmethod
    def _show_characters(cls, target: str):
        characters = cls._get_characters(target)[:4]
        print(f"【{target}】: %s" % [cls.__get_character_show(character, target) for character in characters])

    @classmethod
    def _get_characters(cls, target: str = '') -> typing.List[Character]:
        """获取性格列表"""
        if cls._characters is None:
            # 取数之前需要将子类导入
            ImportUtil.import_module(Path(__file__).parent.joinpath("profile\\characters.py"))
            cls._characters = [character() for character in Character.__subclasses__()]
        if not target:
            return cls._characters
        # 获取目标性格列表
        return sorted(cls._characters, key=lambda x: cls.__get_character_attribute(x, target), reverse=True)

    @staticmethod
    def __get_character_attribute(character: Character, target: str) -> any:
        target = TextualUtil.chinese_to_object_name(target)
        assert getattr(Character(), target) is not None
        return getattr(character, target)

    @classmethod
    def __get_character_show(cls, character: Character, target: str) -> str:
        return f"{character.name}{character.level}({cls.__get_character_attribute(character, target)}%)"
