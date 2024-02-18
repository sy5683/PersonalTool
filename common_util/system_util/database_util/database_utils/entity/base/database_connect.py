import abc
import logging
import traceback


class DatabaseConnect(metaclass=abc.ABCMeta):

    def __init__(self, name: str = ''):
        self.name = name
        self.connect = None
        self.cursor = None

    def __enter__(self):
        logging.info(f"连接数据库: {self.name}")
        try:
            self._get_connect()
        except Exception as e:
            logging.error(f"连接数据库失败: {traceback.format_exc()}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connect is not None:
            logging.info(f"关闭数据库连接: {self.name}")
            self.connect.close()
            self.connect = None

    def execute_sql(self, sql: str):
        """执行sql语句"""
        assert self.connect is not None, "数据库未连接"
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
        """连接数据库"""
