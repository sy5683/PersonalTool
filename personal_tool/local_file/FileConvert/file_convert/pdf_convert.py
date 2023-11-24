import logging
import re
import traceback
import uuid
from pathlib import Path

import fitz

from .feature.file_feature import FileFeature


class PdfConvert:

    @staticmethod
    def pdf_to_images():
        file_paths = FileFeature.get_file_paths()
        assert len(file_paths) == 1, "pdf转图片时一次只能选择一份文件"
        assert FileFeature.get_suffix() == ".pdf", "选择的文件无法进行pdf转图片操作"
        pdf = fitz.open(file_paths[0])
        pdf_page_size = pdf.pageCount
        for page_num in range(pdf_page_size):
            pdf_page = pdf[page_num]
            trans = fitz.Matrix(2, 2).preRotate(0)  # 图片宽高缩放倍率为2，旋转角度为0
            pdf_image = pdf_page.getPixmap(matrix=trans, alpha=False)
            image_path = FileFeature.get_save_path(f"{str(page_num).zfill(len(str(pdf_page_size)))}.png")
            pdf_image.writePNG(image_path)
        pdf.close()

    @staticmethod
    def images_to_pdf():
        file_paths = FileFeature.get_file_paths()
        pdf = fitz.open()
        assert re.match(r"\.png|\.jpg", FileFeature.get_suffix())
        for image_path in sorted(file_paths, key=lambda x: int(re.sub(r"\D+", "", str(Path(x).stem)) + "0")):
            try:
                image = fitz.open(image_path)  # 打开图片
                pdf_bytes = image.convertToPDF()  # 使用图片创建单页的 PDF
                image_pdf = fitz.open("pdf", pdf_bytes)
                pdf.insertPDF(image_pdf)  # 将当前页插入文档
            except RuntimeError:
                logging.error(traceback.format_exc())
                raise RuntimeError(f"图片异常，pdf保存失败: {image_path}")
        pdf_path = FileFeature.get_save_path(f"temp_file_{str(uuid.uuid4())}.pdf")
        pdf.save(pdf_path)
        pdf.close()
