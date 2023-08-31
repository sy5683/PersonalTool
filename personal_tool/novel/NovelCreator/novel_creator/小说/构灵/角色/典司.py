from ....feature.entity.role import Role


class DianSi(Role):

    def __init__(self):
        super().__init__(role_name="典司")

    def set_role_info(self):
        """设置角色信息"""
        self.persona = """
        恐高的天使，战五渣。
        顶级帅哥，头牌牛郎，很会花言巧语，喜欢用法术伪装成魔术泡妞。
        """
