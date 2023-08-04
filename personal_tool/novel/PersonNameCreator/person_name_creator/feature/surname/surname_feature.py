import random
from pathlib import Path
from typing import List

from personal_tool.novel.PersonNameCreator.person_name_creator.util.list_util import ListUtil
from personal_tool.novel.PersonNameCreator.person_name_creator.util.txt_util import TxtUtil


class SurnameFeature:
    _surnames_path = Path(__file__).parent.joinpath("surnames.txt")
    _table_name = "surname"

    @classmethod
    def get_surname(cls, surname: str = None) -> str:
        """获取姓氏"""
        surnames = cls._get_surnames()
        if surname is None:
            surname = random.choice(surnames)
        else:
            if surname not in surnames:
                surnames.append(surname)
                TxtUtil.txt_write(cls._surnames_path, ",".join(surnames))
        return surname

    @classmethod
    def _get_surnames_path(cls) -> Path:
        """获取姓名文件路径"""
        if not cls._surnames_path.exists():
            TxtUtil.txt_write(cls._surnames_path, "")
        return cls._surnames_path

    @classmethod
    def _get_surnames(cls) -> List[str]:
        """获取所有姓氏"""
        surnames_path = cls._get_surnames_path()
        surnames_str = TxtUtil.txt_read(surnames_path)
        surnames = surnames_str.split(",")
        return ListUtil.list_de_duplicate(surnames)
