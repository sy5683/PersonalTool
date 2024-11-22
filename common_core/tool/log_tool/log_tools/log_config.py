import logging


class LogConfig:
    # 日志输出格式
    formatter = logging.Formatter("[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
