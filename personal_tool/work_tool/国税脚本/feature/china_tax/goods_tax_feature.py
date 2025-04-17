import json
import logging
import pathlib
import time
import typing

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.code_util.selenium_util.selenium_utils.enum.operate_type import OperateType
from common_util.file_util.json_util.json_util import JsonUtil
from ..file_feature import FileFeature


class GoodsTaxFeature:
    _goods_tax_map = None

    @classmethod
    def claw_goods_tax_code(cls):
        """爬取商品和服务税收分类编码"""
        # 1) 切换至指定页签
        SeleniumUtil.switch_window(SeleniumConfig(), "发票开具")
        # 2 展开所有的编码
        cls._expand_code_tree()
        # 3) 获取所有的编码
        goods_tax_codes = cls._get_goods_tax_codes()
        try:
            for goods_tax_code in goods_tax_codes:
                # 获取商品和服务分类简称
                goods_tax_name = cls._get_goods_tax_name(goods_tax_code)
                # 添加商品和服务税收分类编码映射表
                logging.info(f"新的商品和服务分类简称: 【{goods_tax_code}】{goods_tax_name}")
                cls._goods_tax_map[goods_tax_code] = goods_tax_name
        finally:
            cls._goods_tax_map = JsonUtil.sort_json(cls._goods_tax_map)
            JsonUtil.write_json(cls.__get_goods_tax_path(), cls._goods_tax_map)

    @classmethod
    def _expand_code_tree(cls):
        """展开编码树"""
        for _ in range(3):
            # 其实应该是可以不用for循环的，但是在代码逻辑上是没有影响的，仅仅是多了几次异常捕获的等待时间
            # 但是可以防止出现特殊情况，导致捕捉到报错使得脚本结束，从而导致编码爬取不完全
            while True:
                # noinspection PyBroadException
                try:
                    xpath = cls.__get_right_tree_xpath(
                        '/div[@class="t-tree__item t-tree__item--visible"]/span/*[name()="svg"]')
                    SeleniumUtil.click(
                        SeleniumConfig(xpath=xpath, operate_type=OperateType.action, wait_seconds=3, logger=None))
                except AttributeError:
                    time.sleep(1)
                    break
                except Exception:
                    time.sleep(1)
                else:
                    xpath = cls.__get_right_tree_xpath('//div[@class="t-loading__gradient-conic"]')
                    SeleniumUtil.wait_disappear(SeleniumConfig(xpath=xpath, logger=None))

    @classmethod
    def _get_goods_tax_codes(cls) -> typing.List[str]:
        """获取商品和服务分类编码"""
        goods_tax_codes = []
        xpath = cls.__get_right_tree_xpath('/div[@class="t-tree__item t-tree__item--visible"]')
        for element in SeleniumUtil.finds(SeleniumConfig(xpath=xpath, logger=None)):
            goods_tax_code = element.get_attribute("data-value")
            # 过滤已有数据
            if goods_tax_code in cls._get_goods_tax_map():
                continue
            goods_tax_codes.append(goods_tax_code)
        return goods_tax_codes

    @classmethod
    def _get_goods_tax_name(cls, goods_tax_code: str) -> str:
        """获取商品和服务分类简称"""
        for _ in range(3):
            SeleniumUtil.click(SeleniumConfig(xpath=f'//div[@data-value="{goods_tax_code}"]', logger=None))
            SeleniumUtil.wait_disappear(SeleniumConfig())
            networks = SeleniumUtil.get_networks(SeleniumConfig())
            for network in networks[::-1]:  # 从最近的一个network开始获取
                result = json.loads(network['response']['body'])
                data = result['Response']['Data']
                if data['Sphfwssflhbbm']:
                    return data['Spfwjc']
        raise RuntimeError(f"页面异常，未取到对应的商品和服务分类简称: {goods_tax_code}")

    @classmethod
    def _get_goods_tax_map(cls) -> typing.Dict[str, str]:
        """获取商品和服务税收分类编码映射表"""
        if cls._goods_tax_map is None:
            goods_tax_path = cls.__get_goods_tax_path()
            cls._goods_tax_map = JsonUtil.read_json(goods_tax_path) if goods_tax_path.exists() else {}
            JsonUtil.write_json(goods_tax_path, cls._goods_tax_map)
        return cls._goods_tax_map

    @staticmethod
    def __get_goods_tax_path() -> pathlib.Path:
        """获取商品和服务税收分类编码映射表路径"""
        return FileFeature.get_file_path("商品和服务税收分类编码映射表.json")

    @staticmethod
    def __get_right_tree_xpath(xpath: str = '') -> str:
        """获取右侧树中的元素"""
        tree_xpath = '//div[@class="right-container"]//div[@class="t-tree__list"]'
        xpath = xpath if xpath.startswith("/") else f"/{xpath}"
        return f'{tree_xpath}{xpath}' if xpath else tree_xpath
