from .entity.base.connect_base import ConnectBase
from .server_type import ServerType


class ConnectServer:
    _connect_map = {}

    @classmethod
    def get_connect(cls, server_type: ServerType, host: str, port: int, username: str, password: str) -> ConnectBase:
        """获取服务器连接对象"""
        name = f"[{server_type.name}]{host}:{port}"
        if name not in cls._connect_map:
            assert all([username, password]), f"{name}服务器连接未缓存，请输入账号密码"
            connect_class = server_type.to_connect_class()
            cls._connect_map[name] = connect_class(host, port, username, password)
        return cls._connect_map[name]
