import unittest

from personal_tool.spider.CrawlingTemplateFile.crawling_template_file.feature.baidu.baidu_feature import BaiduFeature


class BaiduFeatureTestCase(unittest.TestCase):

    def test_get_baidu_image_url(self):
        baidu_image_url = BaiduFeature._get_baidu_image_url()
        self.assertNotEqual(baidu_image_url, None)
        print(baidu_image_url)
