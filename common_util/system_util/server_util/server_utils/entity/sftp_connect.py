import logging
import os

import paramiko

from .base.connect_base import ConnectBase


class SftpConnect(ConnectBase):

    def __init__(self, host: str, port: int, username: str, password: str):
        super().__init__(host, port, username, password)
        self.sftp = None
        self.transport = None

    def close(self):
        """关闭连接"""
        if self.sftp is not None:
            self.sftp.close()
            self.transport.close()
            self.sftp = None
            self.transport = None

    def exists(self, remote_path: str) -> bool:
        """判断路径是否存在"""
        sftp = self._get_sftp()
        # noinspection PyBroadException
        try:
            _ = sftp.stat(remote_path).st_mtime  # 根据是否可以获取修改时间判断路径是否存在
            return True
        except Exception:
            logging.warning(f"sftp服务器中路径不存在: {remote_path}")
            return False

    def upload(self, local_path: str, remote_path: str):
        """上传文件"""
        sftp = self._get_sftp()
        sftp.chdir(remote_path)
        sftp.put(local_path, os.path.basename(local_path))

    def _get_sftp(self) -> paramiko.SFTPClient:
        """获取sftp连接对象"""
        if not self.sftp:
            logging.info(f"连接sftp服务器: {self._host}:{self._port}")
            self.transport = paramiko.Transport((self._host, self._port))
            self.transport.banner_timeout = 120  # 设置默认超时时间，因为原始值15秒太短了
            self.transport.connect(username=self._username, password=self._password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        return self.sftp
