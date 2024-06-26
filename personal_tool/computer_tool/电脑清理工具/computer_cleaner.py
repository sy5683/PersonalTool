import concurrent
from concurrent import futures

from common_core.base.tool_base import ToolBase
from feature.cleaner.temp_file_cleaner import TempFileCleaner


class ComputerCleaner(ToolBase):

    def __init__(self):
        self.functions = [
            TempFileCleaner.clean_tempdir,  # 清理临时文件夹
        ]

    def main(self):
        pool = futures.ThreadPoolExecutor(len(self.functions), thread_name_prefix='清空文件')
        tasks = []
        for function in self.functions:
            tasks.append(pool.submit(function))
        concurrent.futures.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)


if __name__ == '__main__':
    computer_cleaner = ComputerCleaner()
    computer_cleaner.main()
