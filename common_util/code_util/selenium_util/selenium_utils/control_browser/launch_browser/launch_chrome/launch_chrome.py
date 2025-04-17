import abc
import os
import subprocess
import threading
import time
import typing

from selenium import webdriver, common
from selenium.webdriver.chrome.webdriver import WebDriver

from ..base.launch_base import LaunchBase
from ..download_driver import DownloadDriver
from ....entity.cache_driver import CacheDriver
from ....entity.selenium_config import SeleniumConfig


class LaunchChrome(LaunchBase):
    _driver_map: typing.Dict[int, CacheDriver] = {}

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        driver = selenium_config.driver
        if driver is None:
            driver = cls._driver_map.get(threading.current_thread().ident).driver
        if driver is None:
            return
        # 2.1) 使用selenium自带的quit方法关闭driver
        driver.quit()
        time.sleep(1)  # 等待一秒，确认等待操作执行完成
        # 2.2) 因为经常出现quit之后cmd窗口未关的情况，因此这里使用命令行直接关闭进程
        cls._close_browser_by_cmd(selenium_config)
        # 3) 清除缓存
        for thread_id, cache_driver in list(cls._driver_map.items()):
            if driver == cache_driver.driver:
                del cls._driver_map[thread_id]

    @classmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> typing.Optional[WebDriver]:
        """获取driver"""
        # 1) 返回参数中传入的driver
        if selenium_config.driver:
            cls._get_cache_driver(driver=selenium_config.driver)
            return selenium_config.driver
        # 2) 启动谷歌浏览器
        cache_driver = cls._get_cache_driver()
        if cache_driver.driver is None:
            # 根据debug端口判断是启动还是接管
            if cls._get_debug_port(selenium_config) is None:
                cache_driver.driver = cls._launch_chrome(selenium_config)
            else:
                cache_driver.driver = cls._take_over_chrome(selenium_config)
        return cache_driver.driver

    @classmethod
    def launch_browser_debug(cls, selenium_config: SeleniumConfig):
        """debug启动谷歌浏览器"""
        # 1) 检测debug端口
        debug_port = cls._get_debug_port(selenium_config, True)
        assert debug_port > 0, f"端口号异常: {debug_port}"
        assert not cls._netstat_debug_port_running(debug_port), f"Debug端口被占用: {debug_port}"
        selenium_config.info(f"Debug启动谷歌浏览器: {debug_port}")
        # 2) 获取谷歌浏览器路径
        chrome_path = cls._get_chrome_path(selenium_config)
        # 3) cmd调用命令行debug启动谷歌浏览器
        cmd = [chrome_path, f"--remote-debugging-port={debug_port}"]
        subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='gbk')
        time.sleep(1)  # 等待一秒，确认端口正常启动

    @classmethod
    @abc.abstractmethod
    def _close_browser_by_cmd(cls, selenium_config: SeleniumConfig):
        """命令行关闭浏览器"""
        return cls.__get_subclass()._close_browser_by_cmd(selenium_config)

    @classmethod
    def _get_cache_driver(cls, debug_port: int = None, driver: WebDriver = None, driver_path: str = None):
        # 1) 进程id，一个进程对应一个cache_driver
        thread_id = threading.current_thread().ident
        if thread_id not in cls._driver_map:
            cls._driver_map[thread_id] = CacheDriver()
        # 2) 如果传入对应入参，则更新cache_driver中对应的参数
        cache_driver = cls._driver_map[thread_id]
        if debug_port is not None:
            cache_driver.debug_port = debug_port
        if driver is not None:
            cache_driver.driver = driver
        if driver_path is not None:
            cache_driver.driver_path = driver_path
        return cache_driver

    @classmethod
    def _get_chrome_driver(cls, selenium_config: SeleniumConfig, user_data_dir: str = None) -> WebDriver:
        """获取chrome_driver"""
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")  # 解决DevToolActivePort文件不存在的报错
        options.add_argument("--disable-extensions")  # 设置禁用Chrome浏览器扩展
        # 1.2.1) 直接指定谷歌浏览器路径
        if selenium_config.chrome_path:
            options.binary_location = selenium_config.chrome_path
        # 1.2.2) 设置静默运行
        if selenium_config.headless:
            options.add_argument("--headless")
        # 1.2.3) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3.1) 设置忽略私密链接警告
        options.add_argument("--ignore-certificate-errors")
        # 1.3.2) 设置取消提示受自动控制
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        # 1.4.1) 伪装浏览器请求头
        options.add_argument("lang=zh-CN,zh,zh-TW,en-US,en")
        chrome_version = DownloadDriver.get_chrome_version()
        options.add_argument(
            f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36")
        # 1.4.2) 去掉webdriver痕迹
        options.add_argument("disable-blink-features=AutomationControlled")
        # 1.5) 取消提示和默认下载路径在同一个参数中配置
        prefs = options.experimental_options.get("prefs", {})
        # 1.5.1) 设置取消提示
        prefs.update({'credentials_enable_service': False})  # 设置取消提示保存密码
        prefs.update({'download.prompt_for_download': False})  # 取消提示下载
        # 1.5.2) 设置默认下载路径
        selenium_config.info(f"浏览器下载路径为: {selenium_config.download_path}")
        if os.path.exists(selenium_config.download_path):
            prefs.update({'download.default_directory': selenium_config.download_path})
        # 1.5.3) 设置自动下载网页资源
        prefs.update({'profile.default_content_setting_values.automatic_downloads': 1})
        options.add_experimental_option("prefs", prefs)
        # 1.6) 设置读取用户缓存目录
        if selenium_config.use_user_data:
            if user_data_dir is not None and os.path.exists(user_data_dir):
                options.add_argument(f"--user-data-dir={user_data_dir}")
        # 1.7) 设置禁用弹窗拦截
        options.add_argument("--disable-popup-blocking")
        # 2 启动谷歌浏览器
        return cls.__launch_chrome_driver(selenium_config, options)

    @classmethod
    @abc.abstractmethod
    def _get_chrome_path(cls, selenium_config: SeleniumConfig) -> str:
        """获取谷歌浏览器路径"""
        if selenium_config.chrome_path is not None:
            return selenium_config.chrome_path
        return cls.__get_subclass()._get_chrome_path(selenium_config)

    @classmethod
    def _get_debug_port(cls, selenium_config: SeleniumConfig, return_default: bool = False) -> typing.Optional[int]:
        """获取debug端口"""
        # 1) 获取参数中的debug端口
        if selenium_config.debug_port is not None:
            cls._get_cache_driver(debug_port=selenium_config.debug_port)
            return selenium_config.debug_port
        # 2) 返回默认的debug端口
        default_debug_port = 9222
        # 2.1) 如果需要返回默认的debug端口，则无需进行判断debug端口是否正在运行，直接返回
        if return_default:
            cls._get_cache_driver(debug_port=default_debug_port)
            return default_debug_port
        # 2.2) 检测默认的debug端口是否正在运行，如果正在运行，则返回默认的debug_port
        if cls._netstat_debug_port_running(default_debug_port):
            cls._get_cache_driver(debug_port=default_debug_port)
            return default_debug_port
        # 3) 返回缓存中的debug端口
        return cls._get_cache_driver().debug_port

    @classmethod
    def _get_driver_path(cls, selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 1) 使用参数中的driver_path
        if selenium_config.driver_path:
            cls._get_cache_driver(driver_path=selenium_config.driver_path)
            return selenium_config.driver_path
        # 2) 自动获取下载的driver_path路径
        driver_path = DownloadDriver.get_chrome_driver_path()
        cls._get_cache_driver(driver_path=driver_path)
        return driver_path

    @classmethod
    def _launch_chrome(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动谷歌浏览器"""
        selenium_config.info("启动谷歌浏览器")
        try:
            assert selenium_config.use_user_data
            # 1.1) 获取谷歌浏览器用户缓存路径
            user_data_dir = cls.__get_user_data_path(selenium_config) if selenium_config.user_data_dir is None \
                else selenium_config.user_data_dir
            # 1.2) 获取driver
            driver = cls._get_chrome_driver(selenium_config, user_data_dir)
        except (AssertionError, common.exceptions.InvalidArgumentException,
                common.exceptions.SessionNotCreatedException):
            # 2) 重新获取driver，不加载user_data_dir
            driver = cls._get_chrome_driver(selenium_config)
        # 2.2) 注入伪装脚本
        cls.__inject_camouflage_script(driver)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    @abc.abstractmethod
    def _netstat_debug_port_running(cls, debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        return cls.__get_subclass()._netstat_debug_port_running(debug_port)

    @classmethod
    @abc.abstractmethod
    def _set_special_options(cls, selenium_config: SeleniumConfig, options: webdriver.ChromeOptions):
        """进行一些特殊设置"""
        cls.__get_subclass()._set_special_options(selenium_config, options)

    @classmethod
    def _take_over_chrome(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """接管谷歌浏览器"""
        debug_port = cls._get_debug_port(selenium_config)
        assert cls._netstat_debug_port_running(debug_port), f"当前端口并未启动，无法接管谷歌浏览器: {debug_port}"
        selenium_config.info(f"接管已debug运行的谷歌浏览器，端口: {debug_port}")
        # 1.1) 获取谷歌浏览器设置
        options = webdriver.ChromeOptions()
        # 1.2) 添加debug地址
        options.debugger_address = f"127.0.0.1:{debug_port}"  # 地址为本地，只需要指定端口
        # 2) 接管谷歌浏览器
        driver = cls.__launch_chrome_driver(selenium_config, options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        # 4) 接管切换浏览器页签至最后一个
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)  # 接管切换浏览器之后必须强制等待一会，否则会出现操作无效的问题
        return driver

    @classmethod
    def __get_user_data_path(cls, selenium_config: SeleniumConfig) -> typing.Optional[str]:
        """获取谷歌浏览器用户缓存User Data路径"""
        # 路径列表具有优先级，添加路径时注意顺序
        for user_data_path in [
            # 默认路径
            os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Default"),
            # 有的User Data文件放在谷歌浏览器同级目录中
            os.path.join(os.path.dirname(cls._get_chrome_path(selenium_config)), "User Data", "Default"),
        ]:
            if os.path.exists(user_data_path):
                return user_data_path

    @classmethod
    def __launch_chrome_driver(cls, selenium_config: SeleniumConfig, options: webdriver.ChromeOptions) -> WebDriver:
        """启动谷歌浏览器driver"""
        driver_path = cls._get_driver_path(selenium_config)
        # 开启日志性能监听，用于获取页面中的network请求
        options.set_capability("goog:loggingPrefs", {'performance': "ALL"})
        # 进行一些特殊设置
        cls._set_special_options(selenium_config, options)
        from selenium.webdriver.chrome.service import Service
        return webdriver.Chrome(options=options, service=Service(executable_path=driver_path))

    @staticmethod
    def __inject_camouflage_script(driver: webdriver):
        """注入伪装脚本"""
        # 1) 修改 Array.prototype.filter，过滤掉 "webdriver"
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            const originalFilter = Array.prototype.filter;
            Array.prototype.filter = function(callback, thisArg) {
                return originalFilter.call(this, function(item, index, array) {
                    if (item === "webdriver") {
                        return false;
                    }
                    return callback.call(thisArg, item, index, array);
                });
            };
            """
        })
        # 2) 修改 navigator.plugins，注入伪装的插件信息
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: {}},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    },
                    {
                        0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: {}},
                        description: "",
                        filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                        length: 1,
                        name: "Chrome PDF Viewer"
                    },
                    {
                        0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: {}},
                        1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: {}},
                        description: "",
                        filename: "internal-nacl-plugin",
                        length: 2,
                        name: "Native Client"
                    }
                ],
            });
            """
        })
        # 3) 注入 window.navigator.chrome 对象
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(window, 'navigator', {
                value: new Proxy(navigator, {
                    get: function(target, name) {
                        if (name === 'chrome') {
                            return {
                                runtime: {},
                                loadTimes: function() {},
                                csi: function() {},
                                app: {}
                            };
                        }
                        return target[name];
                    }
                })
            });
            """
        })
        # 4) 重写 WebGLRenderingContext.prototype.getParameter，模拟特定的 GPU 信息
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return "NVIDIA Corporation";
                }
                if (parameter === 37446) {
                    return "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti (0x00001B06) Direct3D11 vs_5_0 ps_5_0, D3D11)";
                }
                return getParameter.call(this, parameter);
            };
            """
        })
        # 5) 修改 navigator.languages，伪装常用语言列表
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'en-US', 'en']
            });
            """
        })
        # 6) 重写 navigator.permissions.query 方法，对于 notifications 返回正常状态
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.__proto__.query = parameters => (
              parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
            );
            """
        })
        # 7) 删除 Selenium 暴露的 "cdc_" 前缀属性
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            for (let key in window) {
                if (key.startsWith('cdc_')) {
                    try {
                        delete window[key];
                    } catch(e) {}
                }
            }
            """
        })

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .launch_chrome_windows import LaunchChromeWindows
            return LaunchChromeWindows
        elif os.name == "posix":
            from .launch_chrome_linux import LaunchChromeLinux
            return LaunchChromeLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
