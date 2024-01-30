import abc
import logging


class DatabaseConnect(metaclass=abc.ABCMeta):

    def __init__(self, name: str = ''):
        self.name = name
        self.connect = None
        self.cursor = None
        self._get_connect()

    def __del__(self):
        logging.info(f"关闭数据库连接: {self.name}")
        if self.cursor is not None:
            self.cursor.close()
        if self.connect is not None:
            self.connect.close()

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

    @abc.abstractmethod
    def _get_connect(self):
        """获取连接"""
