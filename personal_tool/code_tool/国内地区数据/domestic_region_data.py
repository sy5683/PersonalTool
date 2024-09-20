from common_core.base.tool_base import ToolBase
from common_util.data_util.object_util.object_util import ObjectUtil
from feature.region_feature import RegionFeature


class DomesticRegionData(ToolBase):

    def main(self):
        regions = RegionFeature.get_regions()
        ObjectUtil.print_object(regions)


if __name__ == '__main__':
    domestic_region_data = DomesticRegionData()
    domestic_region_data.main()
