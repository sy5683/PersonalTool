import logging
import os
import re
import traceback
import typing
from pathlib import Path

import fitz


class ConvertPdf:
    """转换pdf"""

    @classmethod
    def pdf_to_images(cls, pdf_path: str, save_path: typing.Union[Path, str], suffix: str) -> typing.List[str]:
        """pdf转图片"""
        logging.info(f"开始将pdf文件转换为图片: {pdf_path}")
        save_path = os.path.splitext(pdf_path)[0] if save_path is None else str(save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        image_paths = []
        pdf = fitz.open(pdf_path)
        pdf_size = Path(pdf_path).stat().st_size / 1024 / 1024
        for index in range(pdf.page_count):
            pdf_page = pdf[index]
            image_name = f"{str(index).zfill(len(str(pdf.page_count)))}.%s" % re.sub(r"^\.+", "", suffix)
            image_path = os.path.join(save_path, image_name)
            zoom = round(pdf_size / pdf.page_count * 8)
            cls._page_to_image(pdf_page, image_path, zoom=zoom)
            image_paths.append(image_path)
        pdf.close()
        logging.info(f"成功将pdf文件转换为图片: {save_path}")
        return image_paths

    @staticmethod
    def images_to_pdf(image_paths: typing.List[str], save_path: typing.Union[Path, str]) -> str:
        """图片转pdf"""
        logging.info("开始将图片转换为pdf文件")
        if save_path is None:
            image_path = image_paths[0]
            if len(image_paths) == 1:
                save_path = f"{os.path.splitext(image_path)[0]}.pdf"
            else:
                dir_path = os.path.dirname(image_path)
                save_path = os.path.join(dir_path, f"{os.path.basename(dir_path)}.pdf")
        else:
            save_path = str(save_path)
        pdf = fitz.open()
        for image_path in image_paths:
            try:
                image = fitz.open(image_path)  # 打开图片
                pdf_bytes = image.convert_to_pdf()  # 使用图片创建单页的 PDF
                image = fitz.open("pdf", pdf_bytes)
                pdf.insert_pdf(image)  # 将当前页插入文档
            except RuntimeError:
                logging.error(traceback.format_exc())
                raise AttributeError(f"图片异常，pdf保存失败: {image_path}")
        pdf.save(save_path)
        pdf.close()
        logging.info(f"成功将图片转换为pdf文件: {save_path}")
        return save_path

    @staticmethod
    def _page_to_image(page, image_path: str, zoom: float = 2.0, rotate: float = 0.0):
        """页面转图片"""
        # zoom为缩放倍率，倍率为1的话，转换的图片会非常模糊，因此倍率最好从2往上加
        trans = fitz.Matrix(zoom, zoom).prerotate(rotate)
        image = page.get_pixmap(matrix=trans, alpha=False)
        # PyMuPdf在1.19.0之后的版本中修改了保存图片的方法，不再使用writePNG
        image.save(image_path)
