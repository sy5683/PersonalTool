from common_core.base.test_base import TestBase
from common_util.data_util.enum_util.enum_util import EnumUtil


class EnumUtilTestCase(TestBase):

    def test_dict_enum(self):
        class TestEnum(EnumUtil.DictEnum):
            a = {'name': "A"}
            b = {'name': "B"}

            def to_name(self) -> str:
                return self._to_value("name")

            @classmethod
            def get_by_name(cls, value: str):
                return cls._get_by_key("name", value)

        print(TestEnum.a.to_name())
        print(TestEnum.get_by_name("B"))
