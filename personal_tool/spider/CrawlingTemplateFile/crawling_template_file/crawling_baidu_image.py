import shutil
import time

from .feature.baidu.baidu_feature import BaiduFeature
from .util.file_util import FileUtil
from .util.net_util import NetUtil


class CrawlingTemplateImage:

    @staticmethod
    def crawling_baidu_image(search_word: str, quantity: int = None):
        """爬取百度图片"""
        page_number = 1
        save_path = FileUtil.get_temp_path(search_word)
        while True:
            image_urls = BaiduFeature.search_baidu_image_urls(search_word, page_number)
            if not image_urls:
                break
            for image_url in image_urls:
                download_path = NetUtil.download(image_url, "jpg")
                shutil.move(download_path, save_path.joinpath(download_path.name))
                time.sleep(0.5)
                break
            page_number += 1
            if quantity and len(list(save_path.rglob("*"))) > quantity:
                break
