from .entity.types import Types


class TypeFeature:

    @staticmethod
    def get_(*enemy_types: Types):
        types = [each() for each in Types.__subclasses__()]
        for enemy_type in enemy_types:
            for _type in types:
                attack_restrain = getattr(_type, enemy_type.name)
                # 跳过攻击无效的属性
                if not attack_restrain:
                    continue
                defense_restrain = getattr(enemy_type, _type.name)
                # 跳过
                if attack_restrain == 0.5 and defense_restrain != 2:
                    continue
                print(_type)
