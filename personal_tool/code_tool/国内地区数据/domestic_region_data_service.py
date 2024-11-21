from common_core.base.service_base import ServiceBase
from common_util.interface_util.flask_util.flask_util import FlaskUtil
from feature.region_service import RegionService


class DomesticRegionDataService(ServiceBase):

    def __init__(self):
        super().__init__(FlaskUtil.get_app(self.get_subclass_path().stem))

    def set_route(self):
        # 设置地区接口
        RegionService.set_route(self.app)


if __name__ == '__main__':
    DomesticRegionDataService().run()
