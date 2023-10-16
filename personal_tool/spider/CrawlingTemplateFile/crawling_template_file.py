import enum
import typing

from crawling_template_file.crawling_baidu_image import CrawlingTemplateImage
from crawling_template_file.util.file_util import FileUtil
from crawling_template_file.util.win32_util import Win32Util


class Operations(enum.Enum):
    crawling_baidu_image_urls = CrawlingTemplateImage.crawling_baidu_image_urls
    crawling_baidu_image = CrawlingTemplateImage.crawling_baidu_image


class CrawlingTemplateFile:
    """爬取样本文件"""

    def __init__(self, words: typing.List[str]):
        self.words = words

    def main(self, function, **kwargs):
        try:
            for word in self.words:
                function(search_word=word, **kwargs)
        finally:
            Win32Util.open_file(FileUtil.get_temp_path())


if __name__ == '__main__':
    crawling_template_file = CrawlingTemplateFile(["文档", "证书", "表格", "广告", "合同", "论文", "路牌", "财务报表"])
    crawling_template_file.main(Operations.crawling_baidu_image_urls)
