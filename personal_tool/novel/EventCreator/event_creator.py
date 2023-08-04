from event_creator.feture.event_feature import EventFeature
from event_creator.feture.role_feature import RoleFeature


class EventCreator:
    """事件生成器"""

    def main(self):
        # 获取随机未发生事件
        event = EventFeature.get_undone_event()
        # 获取随机数量角色
        roles = RoleFeature.get_random_roles(event.partake_size)
        # 事件参与角色中补充事件关键角色
        for key_role in event.key_roles:
            if key_role.name not in [role.name for role in roles]:
                roles.append(key_role)

        # 输出
        print(f"发生事件：{event.name}")
        print("参与角色：\n\t%s" % "\n\t".join([role.name for role in roles]))


if __name__ == '__main__':
    event_creator = EventCreator()
    event_creator.main()
