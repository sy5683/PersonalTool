from .control_browser.browser_type import BrowserType


class SeleniumConfig:
    browser_type = BrowserType.chrome  # 浏览器类型，默认为谷歌浏览器
    download_path = "E:\\Download"  # 浏览器下载路径
    headless: bool = False  # 是否无头启动，默认为否
    proxy_ip: str = None  # 代理ip
    wait_seconds = 120  # 等待时间，默认为120秒
