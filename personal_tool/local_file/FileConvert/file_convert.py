from enum import Enum

import win32api

from file_convert.feature.file_feature import FileFeature
from file_convert.pdf_convert import PdfConvert


class Operations(Enum):
    pdf_to_images = PdfConvert.pdf_to_images


class FileConvert:

    def main(self, function=None, **kwargs):
        if function and FileFeature.get_file_paths():
            function(**kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", FileFeature.get_save_path(), "", "", 1)


if __name__ == '__main__':
    file_convert = FileConvert()
    file_convert.main(Operations.pdf_to_images)
