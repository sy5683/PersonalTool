from enum import Enum
from pathlib import Path

from common_core.base.tool_base import ToolBase
from common_util.code_util.import_util.import_util import ImportUtil
from feature.character_feature import CharacterFeature


class Operations(Enum):
    show_characters = CharacterFeature.show_characters


class PalWorldTool(ToolBase):

    def __init__(self):
        ImportUtil.import_modules(Path(__file__).parent.joinpath("feature\\profile\\characters.py"))

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    pal_world_tool = PalWorldTool()
    pal_world_tool.main(Operations.show_characters)
