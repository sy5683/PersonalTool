import logging

import pymysql

from .base.database_connect import DatabaseConnect


class MysqlConnect(DatabaseConnect):
    def __init__(self, ip: str, port: int, database_name: str, username: str, password: str):
        self.ip = ip
        self.port = port
        self.database_name = database_name
        self.username = username
        self.password = password
        super().__init__(f"【MySQL】{self.__get_host()}")

    def _get_connect(self):
        """获取连接"""
        logging.info(f"连接MySQL数据库: {self.__get_host()}")
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.username, password=self.password,
                                       database=self.database_name, charset='utf8')
        self.cursor = self.connect.cursor()

    def __get_host(self) -> str:
        return f"{self.ip}:{self.port}"
