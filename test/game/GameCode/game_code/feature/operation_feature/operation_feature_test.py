import unittest

from personal_tool.game.GameCode.game_code.feature.operation_feature.operation_feature import OperationFeature


class OperationFeatureTestCase(unittest.TestCase):

    def test_get_operation_type(self):
        operation_type = OperationFeature.get_operation_type()
        self.assertNotEqual(operation_type, None)
        print(operation_type)
