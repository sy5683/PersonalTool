from common_core.base.service_base import ServiceBase
from feature.region_service import RegionService


class DomesticRegionDataService(ServiceBase):

    def set_route(self):
        # 设置地区接口
        RegionService.set_route(self.app)


if __name__ == '__main__':
    DomesticRegionDataService().run()
