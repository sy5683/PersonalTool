from typing import List, Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import ProjectExperience


class Project004(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "RPA机器人脚本开发"

    def get_work_character(self) -> str:
        """获取工作角色"""
        return "Python开发工程师"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2020年08月", "至今"

    def get_profile(self) -> str:
        """获取简介"""
        return "根据财务的各种需求，定制开发场景脚本，通过机器人客户端运行，实现客户需要的各种功能，包括但不限于接口页面取数、页面填报、pdf回单解析、excel与word生成等……"

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["Selenium", "win32", "fitz、openpyxl、python-docx等各种业务相关库"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return "至今项目中的场景已有30余个，由我主导开发的场景有一半以上，由我参与的场景有二十余个，涉及财务各种需求，其中有以下各类典型:", \
            "【银行回单补扫】解析银行回单pdf，将关键数据与数据库中数据进行对比，然后将匹配的回单截取并上传至影像系统。", \
            "【银行对账】解析客户提供的银行流水excel，与公司系统中下载的明细账excel进行对比，将匹配情况与差异情况生成比对结果，并根据业务需求生成余额调节表。", \
            "【主数据维护】通过图形匹配定位的方法，模拟键盘鼠标操作，对公司的客户端进行操作，实现填报发布等指定操作。", \
            "【月末结账】根据用户提供的取数配置excel表，依次获取对应的数据并根据配置进行相关计算，最终将所有数据汇总成一个总表输出。", \
            "【发票勾选认证】通过公司接口，获取指定期间发票信息，将信息整理为国税系统规范的excel格式，通过页面操作进入国税系统，并将发票导入进行勾选操作。", \
            "【公文打印】登录公司公文系统，按照用户指定操作，对公文进行办毕、归档操作，然后搜索连接打印机打印已归档的公文。", \
            "【中台数据获取】通过接口、指定内网与外网界面，每天定时收集大量指定数据，将其传入中台系统中间表。", \
            "【营销报表图片上传】根据用户选择的参数，定时进入公司报表系统中指定页面，下载报表图片，将图片处理后上传到服务器指定位置。", \
            "【会计报表编制】根据用户提供的编报说明word模板，获取公允、账面等报表中的指定数据，替换编报说明中的数值，生成新的编报说明word文档。", \
            "【项目招标公告提取】遍历提取各集团指定的招标网站信息，爬取招标页面中文档与pdf，整理提取招标关键信息。", \
            "其余类似场景还有【薪酬分发】、【纳税申报】、【财务数据提取】、【融资平台指定报表取数】、【制单机器人】、...等等。", \
