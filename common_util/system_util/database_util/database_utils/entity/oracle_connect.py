import os
import re

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
        try:
            assert os.path.exists(self.oracle_client_path), "Oracle数据库客户端路径不存在"
            assert not re.search("[\u4e00-\u9fa5]+", self.oracle_client_path), "Oracle数据库客户端路径包含中文"
        except AssertionError as e:
            raise FileExistsError(f"{e}: {self.oracle_client_path}")
        oracledb.init_oracle_client(lib_dir=self.oracle_client_path)
        self.connect = oracledb.connect(f"{self.username}/{self.password}@{self.__get_host()}")
        self.cursor = self.connect.cursor()

    def __get_host(self) -> str:
        return f"{self.ip}:{self.port}/{self.database_name}"
