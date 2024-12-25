from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.controller.controller_feature import ControllerFeature
from feature.enum.controller_type import ControllerType


class Operations(Enum):
    submit = ControllerFeature.submit
    update = ControllerFeature.update


class ProjectControlTool(ToolBase):

    def __init__(self, controller_type: ControllerType):
        super().__init__()
        self.controller_type = controller_type

    def main(self, function):
        function(self.controller_type)


if __name__ == '__main__':
    project_control_tool = ProjectControlTool(ControllerType.github)
    # project_control_tool.main(Operations.submit)
    project_control_tool.main(Operations.update)
