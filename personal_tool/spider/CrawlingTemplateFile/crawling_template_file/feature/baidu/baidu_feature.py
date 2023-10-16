import re
import typing

import requests


class BaiduFeature:
    """百度"""
    _headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    @classmethod
    def search_baidu_image_urls(cls, search_word: str, page_number: int) -> typing.List[str]:
        """查询百度图片url列表"""
        url = cls._get_baidu_image_url(f"/search/acjson?tn=resultjson_com&logid=9047316633247341826&ipn=rj"
                                       f"&ct=201326592&is=&fp=result&queryWord={search_word}&cl=2&lm=-1&ie=utf-8"
                                       f"&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={search_word}"
                                       f"&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force="
                                       f"&pn={page_number}&rn=30&gsm=1e&1616935040863=")
        response = requests.get(url=url, headers=cls._headers)
        # 这里要使用正则来提取页面url
        image_urls = re.findall(r'"thumbURL":"(.*?)"', response.text)
        return [image_url for image_url in image_urls if image_url]

    @staticmethod
    def _get_baidu_image_url(uri: str = '') -> str:
        """百度图片搜索的url"""
        return f"http://image.baidu.com/{uri.strip('/')}"
