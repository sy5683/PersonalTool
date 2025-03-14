import abc
import logging
import os


class PdfParseBase(metaclass=abc.ABCMeta):

    @classmethod
    def _parse(cls, pdf_path: str, parser_base, **kwargs):
        """解析"""
        logging.info(f"解析{parser_base.parser_name}: {pdf_path}")
        pdf_name = os.path.basename(pdf_path)
        parsers = []
        for parser_class in parser_base.__subclasses__():
            parser = parser_class(pdf_path, **kwargs)
            if parser.judge():
                parsers.append(parser)
            else:
                del parser
        if not len(parsers):
            raise ValueError(f"{parser_base.parser_name}【{pdf_name}】无法识别")
        elif len(parsers) > 1:
            parsers_types = "、".join([parser.parser_type for parser in parsers])
            raise ValueError(f"{parser_base.parser_name}【{pdf_name}】匹配多种格式: {parsers_types}")
        else:
            parser = parsers[0]
            logging.info(f"{parser.parser_name}【{pdf_name}】的类型为: {parser.parser_type}")
            parser.parse()  # 调用解析方法
            return parser
