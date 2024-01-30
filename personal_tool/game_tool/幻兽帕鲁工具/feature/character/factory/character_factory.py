from ..entity.character import Character


class CharacterFactory:

    @staticmethod
    def sql_data_to_character(data: dict) -> Character:
        character = Character(data['名称'], data['等级'])
        character.gong_ji = data.get("攻击", 0)
        character.fang_yu = data.get("防御", 0)
        character.yi_dong_su_du = data.get("移动速度", 0)
        character.gong_zuo_su_du = data.get("工作速度", 0)
        character.bao_fu_xia_jiang_su_du = data.get("饱腹下降速度", 0)
        character.san_zhi_xia_jiang_su_du = data.get("SAN值下降速度", 0)
        return character
