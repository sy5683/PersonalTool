from .entity.base.connect_base import ConnectBase
from .entity.ftp_connect import FtpConnect
from .entity.sftp_connect import SftpConnect


class ConnectServer:
    _connect_map = {}

    @classmethod
    def get_connect(cls, host: str, port: int, username: str, password: str, **kwargs) -> ConnectBase:
        """获取服务器连接对象"""
        ip = f"{host}:{port}"
        sever_type = kwargs.get("sever_type")
        if ip not in cls._connect_map:
            assert all([username, password])
            if sever_type == "sftp":
                connect = FtpConnect(host, port, username, password)
            else:
                connect = SftpConnect(host, port, username, password)
            cls._connect_map[ip] = connect
        return cls._connect_map[ip]
