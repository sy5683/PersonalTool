from ....feature.entity.role import Role


class SuMuJin(Role):

    def __init__(self):
        super().__init__(role_name="苏木槿")

    def set_role_info(self):
        """设置角色信息"""
        self.persona = """
        十七岁，高二。
        两年前与东方灵相遇，之后以插班生身份进入当前的学校。（埋伏笔，苏木槿在学校是校霸，引出设定东方灵是学校校董）
        """
