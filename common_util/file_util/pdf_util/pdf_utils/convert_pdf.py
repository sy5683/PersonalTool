import logging
import os
import re
import traceback
import typing
from pathlib import Path

import cv2
import fitz
import numpy
from PIL import Image


class ConvertPdf:

    @classmethod
    def pdf_to_images(cls, pdf_path: str, save_path: typing.Union[Path, str], suffix: str,
                      dpi: int) -> typing.List[str]:
        """pdf转图片"""
        logging.info(f"开始将pdf文件转换为图片: {pdf_path}")
        save_path = os.path.splitext(pdf_path)[0] if save_path is None else str(save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        image_paths = []
        pdf = fitz.open(pdf_path)
        for index in range(pdf.page_count):
            pdf_page = pdf[index]
            image_name = f"{Path(pdf_path).stem}_{str(index).zfill(len(str(pdf.page_count)))}"
            image_path = os.path.join(save_path, f"{image_name}.%s" % re.sub(r"^\.+", "", suffix))
            pil_image = cls.page_to_pil_image(pdf_page, dpi)
            pil_image.save(image_path, dpi=(dpi, dpi), format='PNG')
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
    def page_to_cv2_image(page, dpi: float, rotate: float = 0.0) -> numpy.ndarray:
        """页面转Cv2图片"""
        trans = fitz.Matrix(dpi / 72, dpi / 72).prerotate(rotate)
        pix_map = page.get_pixmap(matrix=trans, alpha=False)
        data, width, height = pix_map.samples, pix_map.w, pix_map.h
        numpy_data = numpy.frombuffer(data, numpy.uint8)  # 将字节数组转为numpy格式数据
        if len(numpy_data) % (width * height) == 0:
            image = numpy.reshape(numpy_data, (height, width, len(numpy_data) // (width * height)))
        else:
            image = cv2.imdecode(numpy_data, cv2.IMREAD_ANYCOLOR)
        return image if image is None else cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def page_to_pil_image(page, dpi: float, rotate: float = 0.0) -> Image:
        """页面转PIL图片"""
        trans = fitz.Matrix(dpi / 72, dpi / 72).prerotate(rotate)
        pix_map = page.get_pixmap(matrix=trans, alpha=False)
        return Image.frombytes("RGB", (pix_map.width, pix_map.height), pix_map.samples)