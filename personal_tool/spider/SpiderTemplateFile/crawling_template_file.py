from enum import Enum

from crawling_template_file.crawling_baidu_image import CrawlingTemplateImage


class Operations(Enum):
    crawling_baidu_image = CrawlingTemplateImage.crawling_baidu_image


class CrawlingTemplateFile:
    """爬取模板图片"""

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    crawling_template_file = CrawlingTemplateFile()
    crawling_template_file.main(Operations.crawling_baidu_image, query_word="证件")
