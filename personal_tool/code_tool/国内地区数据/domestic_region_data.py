from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.region_feature import RegionFeature


class Operations(Enum):
    get_detail_regions = RegionFeature.get_detail_regions


class DomesticRegionData(ToolBase):

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    domestic_region_data = DomesticRegionData()
    domestic_region_data.main(Operations.get_detail_regions, region_info='长沙')
