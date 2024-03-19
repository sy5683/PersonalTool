import datetime
import logging
import traceback
from pathlib import Path

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.visual_util.dialog_util.dialog_util import DialogUtil


class SeleniumChecker:

    @staticmethod
    def check_chrome_update():
        """检测谷歌浏览器是否更新"""
        logging.info("检测谷歌浏览器是否更新")
        # 获取chrome_driver路径
        try:
            chrome_driver_path = Path(SeleniumUtil.get_chrome_driver_path())
        except Exception as e:
            logging.error(traceback.format_exc())
            DialogUtil.messagebox(f"chrome_driver下载失败: \n    {e}")
        else:
            # 根据文件的创建日期判断文件是否为新下载文件
            create_stamp = chrome_driver_path.stat().st_ctime
            create_datetime = TimeUtil.time_to_datetime(create_stamp)
            if create_datetime.date() == datetime.datetime.now().date():
                logging.info(f"chrome_driver为当日下载的文件: {chrome_driver_path}")
                DialogUtil.messagebox("chrome_driver已更新")
                Win32Util.open_file(chrome_driver_path.parent)
            else:
                logging.info(f"chrome_driver已为最新版本: {chrome_driver_path}")
                # DialogUtil.messagebox("chrome_driver已为最新版本")
