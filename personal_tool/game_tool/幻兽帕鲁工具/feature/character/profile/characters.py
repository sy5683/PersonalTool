from ..entity.character import Character


class ChuanShuo(Character):

    def __init__(self):
        super().__init__("传说", "Ⅲ")
        self.gong_ji = 20  # 攻击
        self.fang_yu = 20  # 防御
        self.yi_dong_su_du = 15  # 移动速度


class DiWang(Character):

    def __init__(self):
        super().__init__("帝王", "Ⅲ")
        self.gong_ji = 20  # 攻击


class XiYou(Character):

    def __init__(self):
        super().__init__("稀有", "Ⅲ")
        self.gong_ji = 15  # 攻击
        self.gong_zuo_su_du = 15  # 工作速度


class XiongMeng(Character):

    def __init__(self):
        super().__init__("凶猛", "Ⅲ")
        self.gong_ji = 20  # 攻击


class WanQiangRouTi(Character):

    def __init__(self):
        super().__init__("顽强肉体", "Ⅲ")
        self.fang_yu = 20  # 防御


class ShenSu(Character):

    def __init__(self):
        super().__init__("神速", "Ⅲ")
        self.yi_dong_su_du = 30  # 移动速度


class GongJiangJingShen(Character):

    def __init__(self):
        super().__init__("工匠精神", "Ⅲ")
        self.gong_zuo_su_du = 50  # 工作速度


class GongZuoKuang(Character):

    def __init__(self):
        super().__init__("工作狂", "Ⅲ")
        self.san_zhi_xia_jiang_su_du: int = 15  # SAN值下降速度


class JieShiDaShi(Character):

    def __init__(self):
        super().__init__("节食大师", "Ⅲ")
        self.bao_fu_xia_jiang_su_du: int = 15  # 饱腹下降速度


class NaoJin(Character):

    def __init__(self):
        super().__init__("脑筋", "Ⅱ")
        self.gong_ji = 30  # 攻击
        self.gong_zuo_su_du = -50  # 工作速度


class YunDongJianJiang(Character):

    def __init__(self):
        super().__init__("运动健将", "Ⅱ")
        self.yi_dong_su_du = 20  # 移动速度


class RenZhen(Character):

    def __init__(self):
        super().__init__("认真", "Ⅱ")
        self.gong_zuo_su_du = 20  # 工作速度


class LingHuo(Character):

    def __init__(self):
        super().__init__("灵活", "Ⅰ")
        self.yi_dong_su_du = 10  # 移动速度


class SheChu(Character):

    def __init__(self):
        super().__init__("社畜", "Ⅰ")
        self.gong_ji = -30  # 攻击
        self.gong_zuo_su_du = 30  # 工作速度

# class _Character(Character):
#
#     def __init__(self):
#         super().__init__("", "ⅠⅡⅢ")
#         self.gong_ji = 0  # 攻击
#         self.fang_yu = 0  # 防御
#         self.yi_dong_su_du = 0  # 移动速度
#         self.gong_zuo_su_du = 0  # 工作速度
#         self.bao_fu_xia_jiang_su_du: int = 0  # 饱腹下降速度
#         self.san_zhi_xia_jiang_su_du: int = 0  # SAN值下降速度
