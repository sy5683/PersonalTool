from selenium.webdriver.edge.webdriver import WebDriver

from .launch_edge import LaunchEdge


class LaunchEdgeLinux(LaunchEdge):

    @classmethod
    def get_driver(cls, **kwargs) -> WebDriver:
        """获取driver"""
        raise FileExistsError("Linux系统中不存在Edge浏览器。")

    @classmethod
    def _get_edge_path(cls) -> str:
        """获取Edge浏览器路径"""
        raise FileExistsError("Linux系统中不存在Edge浏览器。")
