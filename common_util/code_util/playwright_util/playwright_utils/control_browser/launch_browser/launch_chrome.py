import subprocess
import threading
import time
import typing

from playwright.sync_api import *

from .base.launch_base import LaunchBase
from ...entity.playwright_config import PlaywrightConfig


class LaunchChrome(LaunchBase):
    _playwright: typing.Union[Playwright, None] = None
    _driver_map: typing.Dict[int, typing.Tuple[Browser, BrowserContext, Page]] = {}

    @classmethod
    def close_browser(cls, playwright_config: PlaywrightConfig):
        """关闭浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        browser = playwright_config.browser
        if browser is None:
            debug_port = cls.__get_debug_port(playwright_config)
            browser, context, page = cls._driver_map.get(debug_port if debug_port else threading.current_thread().ident)
        if browser is None:
            return
        # 2) 使用playwright自带的close方法关闭browser
        browser.close()
        time.sleep(1)  # 等待一秒，确认等待操作执行完成
        # 3) 清除缓存
        playwright_config.driver = None
        for key, (_browser, _context, _page) in list(cls._driver_map.items()):
            if browser == _browser:
                del cls._driver_map[key]
        cls._playwright.stop()
        cls._playwright = None

    @classmethod
    def get_driver(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """获取句柄browser, context, page"""
        # 1) 返回参数中传入的browser, context, page
        if playwright_config.browser:
            return playwright_config.browser, playwright_config.context, playwright_config.page
        # 2) 获取debug端口
        debug_port = cls.__get_debug_port(playwright_config)
        # 3.1) 获取进程id，并启动谷歌浏览器
        if debug_port is None:
            thread_id = threading.current_thread().ident
            if thread_id not in cls._driver_map:
                cls._driver_map[thread_id] = cls._launch_chrome(playwright_config)
            return cls._driver_map[thread_id]
        # 3.2) 使用debug方式接管谷歌浏览器
        else:
            if debug_port not in cls._driver_map:
                cls._driver_map[debug_port] = cls._take_over_chrome(playwright_config)
            return cls._driver_map[debug_port]

    @classmethod
    def _launch_chrome(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """启动谷歌浏览器"""
        playwright_config.info("启动谷歌浏览器")
        # 1) 生成playwright实例对象
        playwright = cls.__create_playwright()
        # 2.1) 生成谷歌浏览器
        browser = playwright.chromium.launch(
            headless=playwright_config.headless,
            args=[
                "--disable-blink-features=AutomationControlled",  # 去掉webdriver痕迹
                "--start-maximized",  # 最大化窗口启动
            ]
        )
        # 2.2.1) 生成浏览器内容
        context = browser.new_context(no_viewport=True, **playwright.devices['Desktop Chrome'])
        # 2.2.2) 设置context进行伪装
        cls.__set_context(context)
        # 2.3) 生成浏览器页面
        page = context.new_page()
        # 3.1) 设置默认加载超时时间
        page.set_default_navigation_timeout(playwright_config.wait_seconds * 1000)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(page)
        return browser, context, page

    @classmethod
    def _take_over_chrome(cls, playwright_config: PlaywrightConfig) -> typing.Tuple[Browser, BrowserContext, Page]:
        """接管谷歌浏览器"""
        debug_port = cls.__get_debug_port(playwright_config)
        assert cls.__netstat_debug_port_running(debug_port), f"当前端口并未启动，无法接管谷歌浏览器: {debug_port}"
        playwright_config.info(f"接管已debug运行的谷歌浏览器，端口: {debug_port}")
        # 1) 生成playwright实例对象
        playwright = cls.__create_playwright()
        # 2) 接管谷歌浏览器
        browser = playwright.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
        context = browser.contexts[-1]
        page = context.pages[-1]
        # 3.1) 设置默认加载超时时间
        page.set_default_navigation_timeout(playwright_config.wait_seconds * 1000)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(page)
        # 4) 接管切换浏览器页签至最后一个
        page.bring_to_front()  # 激活当前窗口
        time.sleep(0.5)  # 接管切换浏览器之后必须强制等待一会，否则会出现操作无效的问题
        return browser, context, page

    @classmethod
    def __create_playwright(cls) -> Playwright:
        """生成playwright实例对象"""
        if cls._playwright is None:
            cls._playwright = sync_playwright().start()
        return cls._playwright

    @classmethod
    def __get_debug_port(cls, playwright_config: PlaywrightConfig,
                         return_default: bool = False) -> typing.Union[int, None]:
        """获取debug端口"""
        # 1) 获取参数中的debug_port
        if playwright_config.debug_port:
            return playwright_config.debug_port
        # 2) 返回默认的debug_port
        default_debug_port = 9222
        # 2.1) 如果需要返回默认的debug_port，则无需进行判断debug_port是否正在运行，直接返回
        if return_default:
            return default_debug_port
        # 2.2) 检测默认的debug_port是否正在运行，如果正在运行，则返回默认的debug_port
        if cls.__netstat_debug_port_running(default_debug_port):
            return default_debug_port
        # 3) 返回空值
        return None

    @staticmethod
    def __netstat_debug_port_running(debug_port: int) -> bool:
        """判断debug端口是否正在运行"""
        # noinspection PyBroadException
        try:
            cmd = f'netstat -ano | findstr "{debug_port}" | findstr "LISTEN"'
            with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, encoding='gbk') as p:
                return str(debug_port) in p.stdout.read()
        except Exception:
            return False

    @staticmethod
    def __set_context(context: BrowserContext):
        """设置context进行伪装"""
        # 赋予权限
        context.grant_permissions(["geolocation", "camera", "microphone", "notifications"])
        # webdriver
        context.add_init_script("""
                // 修改 Array.prototype.filter，让它自动过滤掉 "webdriver"
                const originalFilter = Array.prototype.filter;
                Array.prototype.filter = function(callback, thisArg) {
                    return originalFilter.call(this, function(item, index, array) {
                        // 如果元素是 "webdriver"，则忽略它
                        if (item === "webdriver") {
                            return false;  // 过滤掉 "webdriver"
                        }
                        return callback.call(thisArg, item, index, array);
                    });
                };
            """)
        # 注入 JavaScript 修改 navigator.plugins
        context.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
                            description: "",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        },
                        {
                            0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: Plugin},
                            1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: Plugin},
                            description: "",
                            filename: "internal-nacl-plugin",
                            length: 2,
                            name: "Native Client"
                        }
                    ],
                });
            """)
        context.add_init_script("""
                    window.navigator.chrome = {
                        runtime: {},
                        loadTimes: function() {},
                        csi: function() {},
                        app: {}
                    };
                """)
        context.add_init_script("""
                    // 重写 WebGLRenderingContext 的 getParameter 方法
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function (parameter) {
                        // 模拟特定的 WebGL 渲染器和供应商信息
                        if (parameter === 37445) {  // UNMASKED_VENDOR_WEBGL
                            return "NVIDIA Corporation";
                        }
                        if (parameter === 37446) {  // UNMASKED_RENDERER_WEBGL
                            return "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti (0x00001B06) Direct3D11 vs_5_0 ps_5_0, D3D11)";
                        }
                        return getParameter.call(this, parameter);
                    };
                """)
