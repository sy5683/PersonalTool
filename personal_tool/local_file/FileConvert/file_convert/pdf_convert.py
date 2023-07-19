import uuid
from pathlib import Path
from typing import List

import fitz

from .feature.file_feature import FileFeature


class PdfConvert:

    @classmethod
    def pdf_convert(cls):
        file_paths = FileFeature.get_file_paths()
        suffix = FileFeature.get_suffix()
        if len(file_paths) == 1:
            if suffix == ".pdf":
                cls._pdf_to_images(file_paths[0])
        else:
            if suffix == ".png":
                cls._images_to_pdf(file_paths)

    @staticmethod
    def _pdf_to_images(pdf_path: str):
        pdf = fitz.open(pdf_path)
        pdf_page_size = pdf.pageCount
        for page_num in range(pdf_page_size):
            pdf_page = pdf[page_num]
            trans = fitz.Matrix(2, 2).preRotate(0)  # 图片宽高缩放倍率为2，旋转角度为0
            pdf_image = pdf_page.getPixmap(matrix=trans, alpha=False)
            image_path = FileFeature.get_save_path(f"{str(page_num).zfill(len(str(pdf_page_size)))}.png")
            pdf_image.writePNG(image_path)
        pdf.close()

    @staticmethod
    def _images_to_pdf(image_paths: List[str]):
        pdf = fitz.open()
        for image_path in sorted(image_paths, key=lambda x: int(Path(x).stem)):
            image = fitz.open(image_path)  # 打开图片
            pdf_bytes = image.convertToPDF()  # 使用图片创建单页的 PDF
            image_pdf = fitz.open("pdf", pdf_bytes)
            pdf.insertPDF(image_pdf)  # 将当前页插入文档
        pdf_path = FileFeature.get_save_path(f"temp_file_{str(uuid.uuid4())}.pdf")
        pdf.save(pdf_path)
        pdf.close()
