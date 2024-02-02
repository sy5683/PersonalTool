from .entity.base.server_connect import ServerConnect


class ConnectServer:

    @staticmethod
    def get_server_connect(**kwargs) -> ServerConnect:
        """获取服务器连接"""

        # 判断逻辑无法判断服务器
        raise ValueError(f"未知的服务器信息: {kwargs}")
