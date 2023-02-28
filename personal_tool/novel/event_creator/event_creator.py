import random

from base.tool_base import ToolBase
from personal_tool.novel.event_creator.feture.entity_feature import EntityFeature


class EventCreator(ToolBase):
    """事件生成器"""

    def main(self):
        # 获取随机未发生事件
        all_events = EntityFeature.get_all_events()
        undone_events = [event for event in all_events if not event.is_done]
        event = random.choice(undone_events)

        # 获取随机数量角色
        all_roles = EntityFeature.get_all_roles()
        roles = random.sample(all_roles, min(len(all_roles), random.randint(1, event.partake_size)))

        # 事件参与角色中补充事件关键角色
        for key_role in event.key_roles:
            if key_role.name not in [role.name for role in roles]:
                roles.append(key_role)
        print(roles)


if __name__ == '__main__':
    event_creator = EventCreator()
    event_creator.main()
