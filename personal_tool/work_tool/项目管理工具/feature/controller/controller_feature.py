from ..enum.controller_type import ControllerType


class ControllerFeature:

    @staticmethod
    def submit(controller_type: ControllerType):
        """提交项目"""
        controller = controller_type.to_controller()
        controller().submit()

    @staticmethod
    def update(controller_type: ControllerType):
        """更新项目"""
        controller = controller_type.to_controller()
        controller().update()
