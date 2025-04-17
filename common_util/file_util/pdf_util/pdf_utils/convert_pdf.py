import logging
import os
import pathlib
import re
import traceback
import typing

import cv2
import fitz
import numpy
from PIL import Image
from reportlab.pdfgen.canvas import Canvas


class ConvertPdf:

    @classmethod
    def pdf_to_images(cls, pdf_path: str, save_path: typing.Union[pathlib.Path, str], suffix: str,
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
            image_name = f"{pathlib.Path(pdf_path).stem}_{str(index).zfill(len(str(pdf.page_count)))}"
            image_path = os.path.join(save_path, f"{image_name}.%s" % re.sub(r"^\.+", "", suffix))
            pil_image = cls.page_to_pil_image(pdf_page, dpi)
            pil_image.save(image_path, dpi=(dpi, dpi), format='PNG')
            image_paths.append(image_path)
        pdf.close()
        logging.info(f"成功将pdf文件转换为图片: {save_path}")
        return image_paths

    @classmethod
    def images_to_pdf(cls, image_paths: typing.List[str], save_path: typing.Union[pathlib.Path, str],
                      operate_type: str) -> str:
        """图片转pdf"""
        if not image_paths:
            raise FileExistsError("图片数量为空，无法生成pdf")
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
        # 实现图片转pdf
        if operate_type == "fitz":
            cls._images_to_fitz_pdf(image_paths, save_path)
        else:
            cls._images_to_reportlab_pdf(image_paths, save_path)
        logging.info(f"成功将图片转换为pdf文件: {save_path}")
        return save_path

    @staticmethod
    def page_to_cv2_image(page, dpi: float, rotate: float = 0.0) -> numpy.ndarray:
        """通过Cv2实现页面转图片"""
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
        """通过PIL实现页面转图片"""
        trans = fitz.Matrix(dpi / 72, dpi / 72).prerotate(rotate)
        pix_map = page.get_pixmap(matrix=trans, alpha=False)
        return Image.frombytes("RGB", (pix_map.width, pix_map.height), pix_map.samples)

    @staticmethod
    def _images_to_fitz_pdf(image_paths: typing.List[str], save_path: str):
        """通过fitz实现图片转pdf"""
        pdf = fitz.open()
        for image_path in image_paths:
            try:
                image = fitz.open(image_path)
                pdf_bytes = image.convert_to_pdf()  # 使用图片创建单页的PDF
                page = fitz.open("pdf", pdf_bytes)  # 根据这个图片生成PDF页对象
                pdf.insert_pdf(page)  # 将PDF页对象插入文档
            except RuntimeError:
                logging.error(traceback.format_exc())
                raise AttributeError(f"图片异常，pdf保存失败: {image_path}")
        pdf.save(save_path)
        pdf.close()

    @staticmethod
    def _images_to_reportlab_pdf(image_paths: typing.List[str], save_path: str):
        """通过reportlab实现图片转pdf"""
        canvas = Canvas(save_path)
        for image_path in image_paths:
            try:
                image = Image.open(image_path)
                width, height = image.size
                canvas.setPageSize((width, height))
                canvas.drawImage(image_path, 0, 0, width=width, height=height)
                canvas.showPage()  # 新建一页
            except RuntimeError:
                logging.error(traceback.format_exc())
                raise AttributeError(f"图片异常，pdf保存失败: {image_path}")
        canvas.save()
