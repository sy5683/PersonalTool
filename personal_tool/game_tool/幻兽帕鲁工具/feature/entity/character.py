class Character:
    """性格"""

    def __init__(self, name: str = '', level: str = ''):
        self.name = name  # 名称
        self.level = level  # 等级
        self.gong_ji: int = 0  # 攻击
        self.fang_yu: int = 0  # 防御
        self.yi_dong_su_du: int = 0  # 移动速度
        self.gong_zuo_su_du: int = 0  # 工作速度
        self.bao_fu_xia_jiang_su_du: int = 0  # 饱腹下降速度
        self.san_zhi_xia_jiang_su_du: int = 0  # SAN值下降速度
