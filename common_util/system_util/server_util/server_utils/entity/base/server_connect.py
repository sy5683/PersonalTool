import abc
import logging


class ServerConnect(metaclass=abc.ABCMeta):

    def __init__(self, name: str = '', **kwargs):
        self.name = name
        self.connect = None
        self._timeout = kwargs.get("timeout", 120)

    def __del__(self):
        if self.connect is not None:
            logging.info(f"关闭服务器连接: {self.name}")
            self.connect.close()
            self.connect = None

    def __enter__(self):
        return self

    @abc.abstractmethod
    def check_remote_path_exists(self, remote_path: str) -> bool:
        """判断服务器路径是否存在"""

    @abc.abstractmethod
    def upload_file(self, local_path: str, remote_path: str):
        """sftp上传文件"""

    @abc.abstractmethod
    def _get_connect(self):
        """获取连接"""
