from common_core.base.tool_base import ToolBase
from feature.resume_feature import ResumeFeature


class ResumeCreator(ToolBase):

    def main(self):
        # 1) 添加标题
        ResumeFeature.add_title()
        # 2) 添加信息
        ResumeFeature.add_info()
        # 3) 添加工作经验
        ResumeFeature.add_work_experience()
        # 4) 添加项目经验
        ResumeFeature.add_project_experience()

        # 保存并展示
        ResumeFeature.resume_show()


if __name__ == '__main__':
    resume_creator = ResumeCreator()
    resume_creator.main()
