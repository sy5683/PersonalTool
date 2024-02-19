import concurrent
from concurrent import futures

from common_core.base.tool_base import ToolBase
from feature.clean_feature import CleanFeature


class ComputerCleaner(ToolBase):

    def __init__(self):
        self.functions = [
            CleanFeature.clean_tempdir(),  # 清理临时文件夹
        ]

    def main(self):
        # 清理文件夹
        pool = futures.ThreadPoolExecutor(len(self.functions), thread_name_prefix='清空文件')
        tasks = []
        for function in self.functions:
            tasks.append(pool.submit(function))
        concurrent.futures.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)


if __name__ == '__main__':
    computer_cleaner = ComputerCleaner()
    computer_cleaner.main()
