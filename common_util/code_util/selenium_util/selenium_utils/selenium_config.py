from .control_browser.browser_type import BrowserType


class SeleniumConfig:
    browser_type = BrowserType.chrome
    download_path = "E:\\Download"
    headless: bool = False
    proxy_ip: str = None
