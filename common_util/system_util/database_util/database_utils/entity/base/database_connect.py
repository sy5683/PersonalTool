import abc
import logging
import traceback
import typing


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

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connect is not None:
            logging.info(f"关闭数据库连接: {self.name}")
            self.connect.close()
            self.connect = None
        if exc_value:
            raise exc_type(exc_value)

    def execute_sql(self, sql: str, *args):
        """执行sql语句"""
        assert self.connect is not None, "数据库未连接"
        try:
            self.cursor.execute(sql, *args)  # 执行SQL语句
            self.connect.commit()  # 提交事务，只有运行了这句话，sql操作才会生效
        except Exception as e:
            logging.error(e)
            self.connect.rollback()  # 回滚操作

    def get_results(self) -> typing.List[typing.Dict[str, any]]:
        """获取运行结果"""
        tags = [column[0] for column in self.cursor.description]
        return [dict(zip(tags, each)) for each in self.cursor.fetchall()]

    @abc.abstractmethod
    def _get_connect(self):
        """连接数据库"""
