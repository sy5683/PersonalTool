from ....feature.entity.role import Role


class DongFangLing(Role):

    def __init__(self):
        super().__init__(role_name="东方灵")

    def set_role_info(self):
        """设置角色信息"""
        self.persona = """
        二十岁，大二但是未上学，后续需要开学院线直接读大四参加全国大赛和世界联赛。
        """
