from nlp.feature.cut.jieba_feature import JiebaFeature


class NLP:

    def main(self, message: str):
        """"""
        # 1) 分词
        results = JiebaFeature.cut(message)
        print(results)


if __name__ == '__main__':
    nlp = NLP()
    nlp.main("测试语句。")
