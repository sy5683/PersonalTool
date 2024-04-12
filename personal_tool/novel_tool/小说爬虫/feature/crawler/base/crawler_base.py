import abc
import typing
from pathlib import Path


class CrawlerBase(metaclass=abc.ABCMeta):

    def __init__(self, name: str, save_path: typing.Union[Path, str]):
        self.name = name
        self.save_path = str(save_path)

    @abc.abstractmethod
    def run(self, **kwargs):
        """"""
