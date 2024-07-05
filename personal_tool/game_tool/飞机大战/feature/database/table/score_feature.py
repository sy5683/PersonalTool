import typing

from common_util.data_util.time_util.time_util import TimeUtil
from .database_connect_feature import DatabaseConnectFeature
from ..entity.score import Score
from ..factory.score_factory import ScoreFactory


class ScoreFeature:
    _table_name = "Score"

    @classmethod
    def get_scores(cls, username: str) -> typing.List[Score]:
        """获取得分列表"""
        database_connect = DatabaseConnectFeature.get_database_connect()
        with database_connect:
            database_connect.execute_sql(
                f"SELECT * FROM {cls._table_name}%s;" % (f"WHERE username='{username}'" if username else ""))
            results = database_connect.get_results()
            scores = [ScoreFactory.data_to_score(result) for result in results]
            return sorted(scores, key=lambda x: x.score, reverse=True)

    @classmethod
    def save_score(cls, username: str, score: int):
        """保存得分"""
        database_connect = DatabaseConnectFeature.get_database_connect()
        with database_connect:
            database_connect.execute_sql(f"INSERT INTO {cls._table_name} (username, score, save_time) "
                                         f"VALUES ('{username}', '{score}', '{TimeUtil.get_now()}')")
