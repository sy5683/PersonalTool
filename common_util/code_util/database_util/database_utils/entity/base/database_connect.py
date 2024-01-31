import abc
import logging
import traceback

import cx_Oracle


class DatabaseConnect(metaclass=abc.ABCMeta):

    def __init__(self, name: str = ''):
        self.name = name
        self.connect = None
        self.cursor = None
        try:
            self._get_connect()
        except Exception as e:
            logging.error(f"连接数据库失败: {traceback.format_exc()}")
            raise e

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connect is not None:
            logging.info(f"关闭数据库连接: {self.name}")
            self.connect.close()
            self.connect = None

    def __enter__(self):
        return self

    def execute_sql(self, sql: str):
        """执行sql语句"""
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)  # 执行SQL语句
            self.connect.commit()  # 提交事务，只有运行了这句话，sql操作才会生效
        except Exception as e:
            logging.error(e)
            self.connect.rollback()  # 回滚操作

    def get_result(self) -> any:
        """获取运行结果"""
        return self.cursor.fetchone()

    def get_results(self) -> any:
        """获取运行结果"""
        return self.cursor.fetchall()

    @abc.abstractmethod
    def _get_connect(self):
        """获取连接"""
