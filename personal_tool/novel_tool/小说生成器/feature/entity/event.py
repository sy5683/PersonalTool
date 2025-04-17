import abc
import sys


class Event(metaclass=abc.ABCMeta):
    """事件"""

    def __init__(self):
        self.event_path = pathlib.Path(sys.modules[self.__module__].__file__)
        self._event_name = self.event_path.stem  # 事件名称
        self.is_done = False  # 是否完成
        self.key_roles = []  # 关键角色
        self.partake_size = 9  # 事件参与人数
        self.title = """"""  # 标题
        self.text = """"""  # 正文

        # 设置事件信息
        self._set_event_info()
        self.__check_event_info()
        # 设置正文
        self._set_event_content()
        self.__format_text()
        self.__check_event_content()

    @abc.abstractmethod
    def _set_event_info(self):
        """设置事件信息"""

    @abc.abstractmethod
    def _set_event_content(self):
        """设置事件内容"""

    def __check_event_info(self):
        """校验事件信息"""

    def __format_text(self):
        """整理正文"""
        text_list = [each.strip() for each in self.text.split("\n")]
        text = "\n".join([f"\t{each}" for each in text_list])
        self.text = f"\t{text.strip()}"

    def __check_event_content(self):
        """校验事件内容"""
        assert self.title, f"事件【{self._event_name}】中未设置标题"
        assert self.text, f"事件【{self._event_name}】中未写入正文"
