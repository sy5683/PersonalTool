from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.character_feature import CharacterFeature


class Operations(Enum):
    show_characters = CharacterFeature.show_characters


class PalWorldTool(ToolBase):

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    pal_world_tool = PalWorldTool()
    pal_world_tool.main(Operations.show_characters)
