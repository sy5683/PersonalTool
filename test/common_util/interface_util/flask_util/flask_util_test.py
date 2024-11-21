from common_core.base.test_base import TestBase
from common_util.interface_util.flask_util.flask_util import FlaskUtil


class FlaskUtilTestCase(TestBase):

    def setUp(self):
        self.app = FlaskUtil.get_app()

    def test_(self):
        @self.app.route("/test", methods=["GET", "POST"])
        def test():
            return "test"

        FlaskUtil.run(self.app)
