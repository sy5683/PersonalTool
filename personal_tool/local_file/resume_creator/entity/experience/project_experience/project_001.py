from typing import List, Tuple

from personal_tool.local_file.resume_creator.entity.base.experience_base import ProjectExperience


class Project001(ProjectExperience):

    def get_project_name(self) -> str:
        """获取项目名称"""
        return "阅卷系统的图像处理相关支持"

    def get_work_character(self) -> str:
        """获取工作角色"""
        return "Python开发工程师"

    def get_date_range(self) -> Tuple[str, str]:
        """获取开始时间与结束时间"""
        return "2019年09月", "2019年12月"

    def get_profile(self) -> str:
        """获取简介"""
        return "该项目是对于公司项目“阅卷系统”的OCR相关功能的开发。" \
               "为了满足公司需求，提升识别准确度并降低调用接口的费用，在调用百度API接口之前需要对试卷答案进行特殊处理。" \
               "同时因为选择判断题的体量并不需要用到过于强大的OCR，因此还专门对选择判断题进行单独训练。"

    def get_technologies(self) -> List[str]:
        """获取开发技术"""
        return ["OpenCV", "TensorFlow"]

    def get_project_details(self) -> tuple:
        """获取项目明细"""
        return "整理统计各大OCR厂商，调用其OCR接口进行测试，评估准确率与性价比，最后将材料结果整理给领导。", \
            "为了提高OCR准确率，对扫描之后的试卷进行裁剪、校正、截选正确答案、降噪等一系列的操作。为了降低接口调用成本，将截选之后的正确答案根据约定格式，组合生成一张图片，缩减接口调用次数。", \
            "因为百度API的识别范围太过巨大，对选择判断题的需求满足过量，导致在特定要求的识别准确率反而较低，因此专门对选择判断题的进行识别模型训练，实现模型调用接口。"
