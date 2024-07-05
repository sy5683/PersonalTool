from ..entity.score import Score


class ScoreFactory:

    @staticmethod
    def data_to_score(data: dict) -> Score:
        score = Score()
        score.username = data['username']
        score.score = data['score']
        score.save_time = data['save_time']
        return score
