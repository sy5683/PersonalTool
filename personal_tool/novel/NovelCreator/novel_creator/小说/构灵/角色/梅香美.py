from ....feature.entity.role import Role


class MeiXiangMei(Role):

    def __init__(self):
        super().__init__(role_name="梅香美")

    def set_role_info(self):
        """设置角色信息"""
        self.persona = "女神"
