from .server_utils.connect_server import ConnectServer
from .server_utils.entity.base.server_connect import ServerConnect


class ServerUtil:

    @staticmethod
    def get_server_connect(**kwargs) -> ServerConnect:
        """获取服务器连接"""
        return ConnectServer.get_server_connect(**kwargs)
