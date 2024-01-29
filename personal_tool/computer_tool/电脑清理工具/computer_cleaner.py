import concurrent
import tempfile
from concurrent import futures

from common_core.base.tool_base import ToolBase
from feature.clean_feature import CleanFeature


class ComputerCleaner(ToolBase):

    def __init__(self):
        self.clean_dirs = [
            tempfile.gettempdir()  # 临时文件夹
        ]

    def main(self):
        # 清理文件夹
        pool = futures.ThreadPoolExecutor(len(self.clean_dirs), thread_name_prefix="清空文件夹")
        tasks = []
        for clean_dir in self.clean_dirs:
            tasks.append(pool.submit(CleanFeature.clean_dir, clean_dir))
        concurrent.futures.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)


if __name__ == '__main__':
    computer_cleaner = ComputerCleaner()
    computer_cleaner.main()
