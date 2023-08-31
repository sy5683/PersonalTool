from ....feature.entity.role import Role


class YouShe(Role):

    def __init__(self):
        super().__init__(role_name="游舎")

    def set_role_info(self):
        """设置角色信息"""
        self.persona = "勇者"
