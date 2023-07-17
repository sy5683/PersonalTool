from game_code.feature.operation_feature.operation_exception import OperationExit
from game_code.feature.operation_feature.operation_feature import OperationFeature
from game_code.feature.operation_feature.operation_type import OperationType
from game_code.feature.sql_feature.sql_feature import SqlFeature


class GameCode:

    def main(self):
        while True:
            operation_type = OperationFeature.get_operation_type()
            if operation_type == OperationType.quit:
                break
            try:
                function = operation_type.to_function()
                function()
            except OperationExit:
                break
        SqlFeature.connect_close()


if __name__ == '__main__':
    game_code = GameCode()
    game_code.main()
