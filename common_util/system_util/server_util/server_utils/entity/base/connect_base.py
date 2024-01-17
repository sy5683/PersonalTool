import abc


class ConnectBase(metaclass=abc.ABCMeta):

    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    @abc.abstractmethod
    def close(self):
        """关闭连接"""

    @abc.abstractmethod
    def exists(self, remote_path: str) -> bool:
        """判断路径是否存在"""

    @abc.abstractmethod
    def upload(self, local_path: str, remote_path: str):
        """上传文件"""
