from .feature.house_plan.base.house_plan import HousePlan
from .feature.profile.base.house import House
from .feature.profile.furniture.冰箱 import Refrigerator
from .feature.profile.furniture.厕所 import Toilet
from .feature.profile.furniture.厨具 import MicrowaveOven
from .feature.profile.furniture.地毯 import Carpet
from .feature.profile.furniture.墙纸 import Wallpaper
from .feature.profile.furniture.床 import Bed
from .feature.profile.furniture.显示器 import Television
from .feature.profile.furniture.柜子 import BedsideTable, Showcase
from .feature.profile.furniture.桌子 import Board, ComputerDesk, TeaTable, ToiletTable, WritingDesk
from .feature.profile.furniture.沙发 import Sofa, AboveFloorSofa
from .feature.profile.furniture.洗衣机 import Washer
from .feature.profile.furniture.淋浴间 import Shower
from .feature.profile.furniture.游戏机 import PS5, Switch
from .feature.profile.furniture.灶台 import CookingBench
from .feature.profile.furniture.电脑 import Computer
from .feature.profile.furniture.空调 import AirCondition, HangingAirCondition
from .feature.profile.furniture.马桶 import Commode
from .feature.profile.room.卧室 import MasterBedroom, SecondBedroom
from .feature.profile.room.卫生间 import MasterCloakRoom, GuestCloakRoom
from .feature.profile.room.厨房 import Kitchen
from .feature.profile.room.客厅 import LivingRoom
from .feature.profile.room.电竞房 import ComputerRoom
from .feature.profile.room.阳台 import Balcony
from .feature.profile.room.餐厅 import DiningRoom


class HousePlan001(HousePlan):

    @staticmethod
    def get_plan() -> House:
        house = House()

        # 1) 主卧
        master_bedroom = MasterBedroom()
        master_bedroom.add_furniture(Bed(6000))  # 床
        master_bedroom.add_furniture(BedsideTable(1000))  # 床头柜
        master_bedroom.add_furniture(HangingAirCondition(4000))  # 挂式空调
        # master_bedroom.add_furniture(LifeSizeGarageKits(30000))  # 等身大手办
        # master_bedroom.add_furniture(Showcase(1000))  # 等身大手办展示柜
        master_bedroom.add_furniture(WritingDesk(3000))  # 书桌
        house.add_room(master_bedroom)

        # 2) 客厅
        living_room = LivingRoom()
        living_room.add_furniture(Television(8000))  # 电视
        living_room.add_furniture(Sofa(4000))  # 沙发
        living_room.add_furniture(TeaTable(3000))  # 茶几
        living_room.add_furniture(AirCondition(10000))  # 空调
        house.add_room(living_room)

        # 3) 电脑房
        computer_room = ComputerRoom()
        computer_room.add_furniture(ComputerDesk(2000))  # 电脑桌
        computer_room.add_furniture(Computer(15000).bought())  # 电脑
        computer_room.add_furniture(PS5(5000).bought())  # PS5
        computer_room.add_furniture(Switch(5000).bought())  # Switch
        # computer_room.add_furniture(Projector(8000))  # 投影仪
        computer_room.add_furniture(Television(5000))  # 电视
        computer_room.add_furniture(Showcase(2000))  # 展示柜
        computer_room.add_furniture(HangingAirCondition(3000))  # 挂式空调
        computer_room.add_furniture(Wallpaper(400))  # 墙纸
        computer_room.add_furniture(Carpet(800))  # 地毯
        computer_room.add_furniture(AboveFloorSofa(600))  # 地上沙发
        house.add_room(computer_room)

        # 餐厅
        dining_room = DiningRoom()
        dining_room.add_furniture(Board(6000))  # 餐桌
        house.add_room(dining_room)

        # 厨房
        kitchen = Kitchen()
        kitchen.add_furniture(Refrigerator(4000))  # 冰箱
        kitchen.add_furniture(CookingBench(8000))  # 灶台
        kitchen.add_furniture(MicrowaveOven(2000))  # 微波炉
        house.add_room(kitchen)

        # 主卫
        master_cloak_room = MasterCloakRoom()
        master_cloak_room.add_furniture(Shower(5000))  # 淋浴间
        master_cloak_room.add_furniture(ToiletTable(1000))  # 洗漱台
        master_cloak_room.add_furniture(Commode(3000))  # 马桶
        house.add_room(master_cloak_room)

        # 客卫
        guest_cloak_room = GuestCloakRoom()
        guest_cloak_room.add_furniture(Toilet(8000))  # 厕所
        guest_cloak_room.add_furniture(ToiletTable(2000))  # 洗漱台
        house.add_room(guest_cloak_room)

        # 阳台
        balcony = Balcony()
        balcony.add_furniture(Washer(3000))  # 洗衣机
        balcony.add_furniture(Washer(2000))  # 洗衣机
        house.add_room(balcony)

        # 次卧
        second_bedroom = SecondBedroom()
        second_bedroom.add_furniture(Bed(4000))  # 床
        house.add_room(second_bedroom)

        return house
