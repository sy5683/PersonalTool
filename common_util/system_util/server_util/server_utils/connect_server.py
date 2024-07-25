from .entity.base.server_connect import ServerConnect
from .entity.ftp_connect import FtpConnect
from .entity.sftp_connect import SftpConnect


class ConnectServer:

    @staticmethod
    def get_server_connect(**kwargs) -> ServerConnect:
        """获取服务器连接"""
        ip = kwargs.pop("ip")
        port = kwargs.pop("port")
        username = kwargs.pop("username")
        password = kwargs.pop("password")
        server_type = kwargs.pop("server_type", "FTP")
        if server_type == "FTP":
            return FtpConnect(ip, port, username, password, **kwargs)
        elif server_type == "SFTP":
            return SftpConnect(ip, port, username, password, **kwargs)

        # 判断逻辑无法判断服务器
        raise ValueError(f"未知的服务器信息: {kwargs}")
