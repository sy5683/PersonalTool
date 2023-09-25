class CrawlingTemplateImage:

    @staticmethod
    def crawling_baidu_image(query_word: str):
        """爬取百度图片"""
        baidu_url = "http://image.baidu.com"
        url = f"{baidu_url}/search/acjson?tn=resultjson_com&ipn=rj&queryWord={query_word}&word={query_word}&pn=1"
        print(url)
