from base.tool_base import ToolBase
from personal_tool.novel.event_creator.feture.entity_feature import EntityFeature


class EventCreator(ToolBase):
    """事件生成器"""

    def main(self):
        all_roles = EntityFeature.get_all_roles()
        print(all_roles)


if __name__ == '__main__':
    event_creator = EventCreator()
    event_creator.main()
