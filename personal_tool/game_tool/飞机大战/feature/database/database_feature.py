import typing

from .entity.score import Score
from .table.score_feature import ScoreFeature


class DatabaseFeature:

    @staticmethod
    def get_scores(username: str = '') -> typing.List[Score]:
        """获取得分列表"""
        return ScoreFeature.get_scores(username)

    @staticmethod
    def save_score(username: str, score: int):
        """保存得分"""
        ScoreFeature.save_score(username, score)
