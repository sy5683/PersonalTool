import logging
import re
import traceback

from base.tool_base import ToolBase
from personal_tool.fallout.fallout_4_code.config.fallout_4_code_config import sqlite_name, table_name
from personal_tool.fallout.fallout_4_code.util.sqlite_util.sqlite_util import SqliteUtil


class OperationExit(Exception):
    """操作退出"""


class Fallout4Code(ToolBase):
    """辐射4指令代码"""

    def __init__(self):
        self.sqlite_connect = SqliteUtil.get_sqlite_connect(sqlite_name)
        self.operation_maps = (
            {'number': 1, 'name': "添加道具", 'function': self.add_item},
            {'number': 2, 'name': "获取道具指令", 'function': self.get_item_command},
            {'number': 3, 'name': "展示道具", 'function': self.show_items},
        )

    def main(self):
        while True:
            operation_number = self._get_operation_input()
            if operation_number == "q":
                break
            for operation_map in self.operation_maps:
                if int(operation_number) == operation_map.get("number"):
                    while True:
                        # noinspection PyBroadException
                        try:
                            operation_map['function']()
                        except OperationExit:
                            break
                        except Exception:
                            logging.error(traceback.format_exc())
                            break
                    break
            else:
                print(f"错误的操作输入，请重新输入: {operation_number}")
        self.sqlite_connect.close()

    def add_item(self):
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
        select_sql = f"SELECT * FROM {table_name} WHERE item_name='{item_name}';"
        self.sqlite_connect.sql_execute(select_sql)
        results = self.sqlite_connect.get_result()
        if results:
            print(f"道具【{item_name}】已存在")
        else:
            # 3) 将道具代码与道具名称添加至数据库
            insert_sql = f"INSERT INTO {table_name} (item_name, item_code) VALUES ('{item_name}', '{item_code}');"
            self.sqlite_connect.sql_execute(insert_sql)

    def get_item_command(self):
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
        select_sql = f"SELECT item_name, item_code FROM {table_name} WHERE item_name='{item_name}';"
        self.sqlite_connect.sql_execute(select_sql)
        results = self.sqlite_connect.get_result()
        if results:
            # 3.1) 如果查询到指定结果，则显示查询信息
            for result_name, result_code in results:
                print(f"【{result_name}】 {self._get_command(result_code, item_quantity)}")
            # 3.2) 数据库添加其使用次数+1
            update_sql = f"UPDATE {table_name} SET usage_count=usage_count+1 WHERE item_name='{item_name}';"
            self.sqlite_connect.sql_execute(update_sql)
        else:
            # 4.1) 如果没有查询到指定结果，则使用模糊查询再次查询sql，将所有模糊匹配的道具名列出来
            print(f"未找到道具名为【{item_name}】的道具，你要查找的是否为以下道具：")
            select_sql = f"SELECT item_name FROM {table_name} WHERE item_name LIKE '%{item_name}%';"
            self.sqlite_connect.sql_execute(select_sql)
            # 4.2) 只显示名称，为了累计使用次数，必须使用完整的道具名称才能获取命令代码
            for result in self.sqlite_connect.get_result():
                print(f"【{result[0]}】")
            # 4.3) 递归调用方法，重新输入
            self.get_item_command()

    def show_items(self):
        """展示道具"""
        print("================")
        print("【展示道具】以下为所有已知代码列表")
        select_order_sql = f"SELECT item_name, item_code FROM {table_name} ORDER BY usage_count DESC;"
        self.sqlite_connect.sql_execute(select_order_sql)
        results = self.sqlite_connect.get_result()
        for result_name, result_code in results:
            print(f"【{result_name}】 {result_code}")
        raise OperationExit()

    def _get_operation_input(self):
        """获取操作输入"""
        print("=====操作列表=====")
        for operation_map in self.operation_maps:
            print(f"【{operation_map.get('name')}】: {operation_map.get('number')}")
        return input("请输入操作，q退出：")

    @staticmethod
    def _get_command(item_code: str, item_quantity: int = None) -> str:
        """生成指令"""
        command = f"player.additem {item_code} %d"
        return command if item_quantity is None else command % int(item_quantity)


if __name__ == '__main__':
    fallout_4_code = Fallout4Code()
    fallout_4_code.main()
