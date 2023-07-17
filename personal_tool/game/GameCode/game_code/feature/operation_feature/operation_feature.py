from .operation_type import OperationType


class OperationFeature:

    @classmethod
    def get_operation_type(cls) -> OperationType:
        """获取操作id"""
        print("=====操作列表=====")
        for operation_type in OperationType:
            print(f"{operation_type.to_id()}. {operation_type.to_name()}")
        operation_id = input("请输入操作id，q退出：")
        for operation_type in OperationType:
            if operation_type.to_id() == operation_id:
                return operation_type
        else:
            print(f"错误的操作输入，请重新输入: {operation_id}")
            return cls.get_operation_type()
