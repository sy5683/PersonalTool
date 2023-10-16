import enum
import re

from .operation_exception import OperationExit
from ..sql_feature.sql_feature import SqlFeature


class Operations:

    @staticmethod
    def add_item():
        """添加道具"""
        # 1) 获取道具代码与道具名称
        print("================")
        item_input = input("准备【添加道具】，请输入道具代码和道具名称（中间使用空格隔开）：\n").strip()
        if item_input == "q":
            raise OperationExit()
        item_code, item_name = item_input.split(" ")
        if re.search(r"[\u4e00-\u9fa5]+", item_code):
            raise ValueError("输入的道具代码异常，请确认顺序")

        # 2) 查询道具是否已存在
        results = SqlFeature.find_item(item_name)
        if results:
            print(f"道具【{item_name}】已存在")
        else:
            # 3) 将道具代码与道具名称添加至数据库
            SqlFeature.add_item(item_name, item_code)

    @classmethod
    def get_item_command(cls):
        """获取道具指令"""
        # 1) 获取道具名称与指定数量
        print("================")
        item_input = input("准备【获取道具指令】，请输入道具名称与指定数量（数量可以不输入，中间使用空格隔开）：\n").strip()
        if item_input == "q":
            raise OperationExit()
        if re.search(" ", item_input):
            item_name, item_quantity = item_input.split(" ")
            if not item_quantity.isdigit():
                raise ValueError("输入的指定数量异常，请确认输入为纯数字")
        else:
            item_name, item_quantity = item_input, None

        # 2) 查询指定名称的道具
        result = SqlFeature.find_item(item_name)
        if result:
            # 3.1) 如果查询到指定结果，则显示查询信息
            print(f'【{result[0]}】 "player.additem {result[1]} %d"')
            # 3.2) 数据库添加其使用次数+1
            SqlFeature.add_usage_count(item_name)
        else:
            # 4.1) 如果没有查询到指定结果，则使用模糊查询再次查询sql，将所有模糊匹配的道具名列出来
            print(f"未找到道具名为【{item_name}】的道具，你要查找的是否为以下道具：")
            for result_name, result_code in SqlFeature.find_items(item_name):
                # 4.2) 只显示名称，为了累计使用次数，必须使用完整的道具名称才能获取命令代码
                print(f"【{result_name}】")
            # 4.3) 递归调用方法，重新输入
            cls.get_item_command()

    @staticmethod
    def show_items():
        """展示道具"""
        print("================")
        print("【展示道具】以下为所有已知代码列表")
        for result_name, result_code in SqlFeature.find_items():
            print(f"【{result_name}】 {result_code}")


class OperationType(enum.Enum):
    add_item = {'id': "1", 'name': "添加道具", 'function': Operations.add_item}
    get_item_command = {'id': "2", 'name': "获取道具指令", 'function': Operations.get_item_command}
    show_items = {'id': "3", 'name': "展示道具", 'function': Operations.show_items}
    quit = {'id': "q", 'name': "退出程序"}

    def to_id(self) -> str:
        return self.value['id']

    def to_name(self) -> str:
        return self.value['name']

    def to_function(self):
        return self.value['function']
