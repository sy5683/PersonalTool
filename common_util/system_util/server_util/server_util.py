from .server_utils.connect_server import ConnectServer
from .server_utils.entity.base.connect_base import ConnectBase
from .server_utils.server_type import ServerType


class ServerUtil:

    @staticmethod
    def get_connect(server_type: ServerType, host: str, port: int,
                    username: str = None, password: str = None) -> ConnectBase:
        """获取服务器连接对象"""
        return ConnectServer.get_connect(server_type, host, port, username, password)
