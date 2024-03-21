import os

import oracledb

from .base.database_connect import DatabaseConnect


class OracleConnect(DatabaseConnect):

    def __init__(self, ip: str, port: int, database_name: str, username: str, password: str, oracle_client_path: str):
        self.ip = ip
        self.port = port
        self.database_name = database_name
        self.username = username
        self.password = password
        self.oracle_client_path = oracle_client_path
        super().__init__(f"【Oracle】{self.__get_host()}")

    def _get_connect(self):
        """连接数据库"""
        # 设置oracle客户端路径，客户端路径不能为中文
        if os.path.exists(self.oracle_client_path):
            oracledb.init_oracle_client(lib_dir=self.oracle_client_path)
        self.connect = oracledb.connect(f"{self.username}/{self.password}@{self.__get_host()}")
        self.cursor = self.connect.cursor()

    def __get_host(self) -> str:
        return f"{self.ip}:{self.port}/{self.database_name}"
