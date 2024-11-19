import abc
import sys
from pathlib import Path

from common_util.interface_util.flask_util.flask_util import FlaskUtil
from .log_base import LogBase


class ServiceBase(LogBase, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()
        service_name = Path(sys.modules[self.__module__].__file__).parent.name
        self.app = FlaskUtil.get_app(service_name)

    @abc.abstractmethod
    def set_route(self, *args, **kwargs):
        """设置接口服务"""

    def run(self):
        """服务器启动方法"""
        self.set_route()
        FlaskUtil.run(self.app)
