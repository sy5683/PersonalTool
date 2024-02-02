import logging
import os

import paramiko

from .base.server_connect import ServerConnect


class SftpConnect(ServerConnect):

    def __init__(self, ip: str, port: int, username: str, password: str, **kwargs):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self._transport = None
        super().__init__(f"【SFTP】{self.__get_host()}", **kwargs)

    def __del__(self):
        super().__del__()
        if self._transport is not None:
            self._transport.close()
            self._transport = None

    def check_remote_path_exists(self, remote_path: str) -> bool:
        """判断服务器路径是否存在"""
        # noinspection PyBroadException
        try:
            # 根据是否可以获取修改时间判断路径是否存在
            _ = self.connect.stat(remote_path).st_mtime
            return True
        except Exception:
            return False

    def upload_file(self, local_path: str, remote_path: str):
        """sftp上传文件"""
        self.connect.chdir(remote_path)
        self.connect.put(local_path, os.path.basename(local_path))

    def _get_connect(self):
        """获取连接"""
        logging.info(f"连接SFTP服务器: {self.__get_host()}")
        self._transport = paramiko.Transport((self.ip, self.port))
        self._transport.banner_timeout = self._timeout
        self._transport.connect(username=self.username, password=self.password)
        self.connect = paramiko.SFTPClient.from_transport(self._transport)

    def __get_host(self) -> str:
        return f"{self.ip}:{self.port}"
