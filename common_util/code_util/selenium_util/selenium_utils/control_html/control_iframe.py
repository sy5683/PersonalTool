from selenium import webdriver



class ControlIframe:
    """控制iframe"""

    # @staticmethod
    # def switch_iframe(driver: webdriver, xpath: str, wait_seconds: int):
    #     """切换iframe"""
    #     if not xpath:
    #         SeleniumSource.switch_to_default_iframe(driver)
    #     elif xpath == "..":  # 因为元素的父级也是这个xpath，因此这里使用一样的语法处理
    #         SeleniumSource.switch_to_parent_iframe(driver)
    #     else:
    #         iframe = SeleniumSource.find_element_explicitly(driver, xpath, wait_seconds)
    #         SeleniumSource.switch_to_iframe(driver, iframe)
    #     # iframe切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
    #     TimeSource.time_sleep(1)
