import abc

from ...file_feature import FileFeature


class SceneBase(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def main(self):
        """"""
