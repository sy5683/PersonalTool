import re

from ..control_html.control_element import ControlElement


class ControlPdf:

    @staticmethod
    def get_pdf_content(pdf_xpath: str, **kwargs) -> str:
        """获取pdf"""
        # 页面翻页至首页
        page_number_element = ControlElement.find('//span[@id="numPages"]', **kwargs)
        page_number = int(re.sub(r"\D+", "", page_number_element.get_attribute("innerText")))
        previous_button = ControlElement.find('//button[@id="previous"]', **kwargs)  # 上一页按钮
        for _ in range(page_number):
            if not previous_button.is_enabled():
                break
            ControlElement.click(previous_button, **kwargs)
        # 提取文档
        content = ""
        next_button = ControlElement.find('//button[@id="next"]', **kwargs)  # 下一页按钮
        for page_index in range(page_number):
            pdf_xpath = pdf_xpath.format(page_num=page_index + 1)
            pdf_element = ControlElement.find(pdf_xpath, **kwargs)
            content += pdf_element.get_attribute("innerText")
            if not next_button.is_enabled():
                break
            ControlElement.click(next_button, **kwargs)
        # 因为pdf提取的格式异常，因此这里将所有\n替换保证需要匹配的字符串是相邻的
        return content.replace("\n", "")
