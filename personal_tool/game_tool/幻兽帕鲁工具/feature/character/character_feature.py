import typing

from common_util.data_util.textual_util.textual_util import TextualUtil
from .entity.character import Character
from .factory.character_factory import CharacterFactory
from ..database_feature import DatabaseFeature


class CharacterFeature:
    _characters = None
    __table_name = "Character"

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
            database_connect = DatabaseFeature.get_database_connect()
            # 获取表字段列表
            database_connect.execute_sql(f"SELECT name FROM pragma_table_info('{cls.__table_name}');")
            tags = [each[0] for each in database_connect.get_results()]
            # 获取表数据
            database_connect.execute_sql(f"SELECT * FROM Character;")
            cls._characters = []
            for each in database_connect.get_results():
                character = CharacterFactory.sql_data_to_character(dict(zip(tags, each)))
                cls._characters.append(character)
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
