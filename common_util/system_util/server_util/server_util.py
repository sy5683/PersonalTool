from .server_utils.connect_server import ConnectServer
from .server_utils.entity.base.connect_base import ConnectBase


class ServerUtil:

    @staticmethod
    def get_connect(host: str, port: int, username: str = None, password: str = None, **kwargs) -> ConnectBase:
        """获取服务器连接对象"""
        return ConnectServer.get_connect(host, port, username, password)
