from common_core.base.tool_base import ToolBase
from feature.selenium_checker import SeleniumChecker


class TimedChecker(ToolBase):

    def main(self, *args, **kwargs):
        SeleniumChecker.check_chrome_update()


if __name__ == '__main__':
    timed_checker = TimedChecker()
    timed_checker.main()
