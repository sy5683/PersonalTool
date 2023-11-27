import psutil


class PsutilUtil:

    @staticmethod
    def check_process_running(process_name: str) -> bool:
        """判断程序是否运行"""
        for pid in psutil.pids():
            process = psutil.Process(pid)
            if process_name == process.name():
                return True
        return False
