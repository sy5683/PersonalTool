from typing import List, Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import ProjectExperience


class Project004(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "RPA机器人脚本开发"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020-08", ""

    def get_profile(self) -> str:
        """获取简介"""
        return "根据财务的各种需求，定制开发场景脚本，通过机器人客户端运行，实现客户需要的各种功能，包括但不限于接口页面取数、页面填报、pdf回单解析、excel与word生成等……"

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["Selenium", "win32", "其他各种python相关库"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return "至今项目中的场景已有30多个，由我主导开发的场景有一半以上，由我参与的场景有二十余个，涉及财务各种需求，其中有:", \
            "【银行回单补扫】解析银行回单pdf，将关键数据与数据库中数据进行对比，然后将匹配的回单截取并上传至影像系统。", \
            "【银行对账】解析客户提供的银行流水excel，与公司系统中下载的明细账excel进行对比，将匹配情况与差异情况生成比对结果，并根据业务需求生成余额调节表。", \
            "【主数据维护】通过图形匹配定位的方法，模拟键盘鼠标操作，对公司的客户端进行操作，实现填报发布等指定操作。", \
            "【月末结账】", \
            "【薪酬分发】", \
            "【发票勾选认证】", \
            "【纳税申报】", \
            "【公文打印】", \
            "【中台数据获取】", \
            "【融资平台指定报表取数】", \
            "【制单机器人】", \
            "【报表图片上传】", \
            "【公文机器人】"
