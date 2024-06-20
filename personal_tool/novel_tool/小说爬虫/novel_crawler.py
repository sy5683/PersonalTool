from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.crawler.crawler_001 import Crawler001


class Operations(Enum):
    crawler_001 = Crawler001


class NovelCrawler(ToolBase):

    def main(self, _class, **kwargs):
        crawler = _class.value("E:\\test.txt")
        crawler.run(**kwargs)


if __name__ == '__main__':
    novel_crawler = NovelCrawler()
    novel_crawler.main(Operations.crawler_001, url_suffix='/bqg/416616/142035366.html')
