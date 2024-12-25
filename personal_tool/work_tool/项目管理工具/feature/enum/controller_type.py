import typing

from common_util.data_util.enum_util.enum_util import EnumUtil
from ..controller.base.controller_base import ControllerBase

from ..controller.profile.github import Github


class ControllerType(EnumUtil.DictEnum):
    """版本控制方式"""
    github = {'controller': Github}
    # subversion = {'controller': ""}

    def to_controller(self) -> typing.Type[ControllerBase]:
        return self._to_value("controller")