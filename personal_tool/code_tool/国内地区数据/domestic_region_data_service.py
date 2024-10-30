from pathlib import Path

from common_util.interface_util.flask_util.flask_util import FlaskUtil
from feature.region_service import RegionService


class DomesticRegionDataService:

    def __init__(self):
        self.app = FlaskUtil.get_app(Path(__file__).parent.name)

    def main(self):
        RegionService.set_route(self.app)
        FlaskUtil.run(self.app)


if __name__ == '__main__':
    domestic_region_data_service = DomesticRegionDataService()
    domestic_region_data_service.main()
