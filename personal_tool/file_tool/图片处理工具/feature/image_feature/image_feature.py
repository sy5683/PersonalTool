import typing

from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil


class ImageFeature:

    @staticmethod
    def to_image_paths(file_paths: typing.List[str]):
        image_paths = []
        for file_path in file_paths:
            if FileUtil.get_original_type(file_path) == "pdf":
                image_paths += PdfUtil.pdf_to_images(file_path)
            else:
                image_paths += [file_path]
        return image_paths
