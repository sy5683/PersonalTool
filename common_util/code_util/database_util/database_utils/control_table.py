import typing

from .entity.base.database_connect import DatabaseConnect


class ControlTable:

    @classmethod
    def get_data_list(cls, database_connect: DatabaseConnect, table_name: str) -> typing.List[dict]:
        """获取数据库表数据"""
        tags = cls.get_tags(database_connect, table_name)
        database_connect.execute_sql(f"SELECT * FROM {table_name};")
        data_list = []
        for each in database_connect.get_results():
            data_list.append(dict(zip(tags, each)))
        return data_list

    @staticmethod
    def get_tags(database_connect: DatabaseConnect, table_name: str) -> typing.List[str]:
        """获取表头"""
        database_connect.execute_sql(f"SELECT name FROM pragma_table_info('{table_name}');")
        return [each[0] for each in database_connect.get_results()]
