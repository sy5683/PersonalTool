from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.crawler.crawler_001 import Crawler001
from feature.crawler.crawler_002 import Crawler002


class Operations(Enum):
    crawler_001 = Crawler001
    crawler_002 = Crawler002


class NovelCrawler(ToolBase):

    def main(self, _class, **kwargs):
        crawler = _class.value("E:/test.txt")
        crawler.run(**kwargs)


if __name__ == '__main__':
    novel_crawler = NovelCrawler()
    novel_crawler.main(Operations.crawler_001, url_suffix='/bqg/1248786/310930932.html')
    # novel_crawler.main(Operations.crawler_002, url_suffix='/174/174341/55814489.html')
