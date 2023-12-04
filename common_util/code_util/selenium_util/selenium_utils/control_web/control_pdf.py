from selenium import webdriver

from ..control_html.control_element import ControlElement


class ControlPdf:

    @staticmethod
    def get_pdf_content(driver: webdriver, pdf_xpath: str, wait_seconds: int) -> str:
        """获取pdf"""
        # # 页面翻页至首页
        # element = ControlElement.find_element(driver, '//span[@id="numPages"]', wait_seconds)
        # num_pages = SeleniumSource.get_attribute(element, "innerText")
        # page_number = int(ReSource.re_sub(r"\D+", "", num_pages))
        # # 上一页按钮
        # previous_button = SeleniumSource.find_element_explicitly(driver, '//button[@id="previous"]', wait_seconds)
        # for _ in range(page_number):
        #     if not SeleniumSource.check_element_clickable(previous_button):
        #         break
        #     SeleniumSource.click_element(previous_button)
        #     TimeSource.time_sleep(0.5)
        # # 提取文档
        # content = ""
        # # 下一页按钮
        # next_button = SeleniumSource.find_element_explicitly(driver, '//button[@id="next"]', wait_seconds)
        # for page_index in range(page_number):
        #     pdf_xpath = pdf_xpath.format(page_num=page_index + 1)
        #     pdf_element = SeleniumSource.find_element_explicitly(driver, pdf_xpath, wait_seconds)
        #     content += SeleniumSource.get_attribute(pdf_element, "innerText")
        #     if not SeleniumSource.check_element_clickable(next_button):
        #         break
        #     SeleniumSource.click_element(next_button)
        # # 因为pdf提取的格式异常，因此这里将所有\n替换保证需要匹配的字符串是相邻的
        # return StrSource.replace_str(content, "\n", "")
