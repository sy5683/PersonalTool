from pathlib import Path

from common_core.base.tool_base import ToolBase
from common_util.code_util.import_util.import_util import ImportUtil
from feature.profile.types.幽灵 import Ghost
from feature.type_feature import TypeFeature


class Pokemen(ToolBase):

    def __init__(self):
        ImportUtil.import_modules(Path(__file__).parent)

    def main(self):
        """"""
        TypeFeature.get_(Ghost())


if __name__ == '__main__':
    pokemen = Pokemen()
    pokemen.main()
