import logging
import typing

import cv2
import fitz
import numpy


class ExtractPdf:

    @classmethod
    def get_pdf_images(cls, pdf_path: str) -> typing.List[numpy.ndarray]:
        """提取pdf中图片"""
        pdf = fitz.open(pdf_path)
        # 如果是xps对象需要转为pdf对象，然后提取图片，但是会丢失透明度
        if pdf.name.endswith('xps'):
            pdf_bytes = pdf.convert_to_pdf()
            pdf.close()
            pdf = fitz.open("pdf", pdf_bytes)
        page_images = []
        for index in range(pdf.page_count):
            for item_index, item in enumerate(pdf[index].get_images()):
                image = cls.__recover_pix(pdf, item)
                if isinstance(image, dict):
                    width, height, data = image['width'], image['height'], image['image']
                elif isinstance(image, fitz.Pixmap):
                    width, height, data = image.width, image.height, image.samples
                else:
                    logging.warning(f"pdf中图片异常：第{index + 1}页第{item_index + 1}张")
                    continue
                # 转为cv2格式的图片
                page_images.append(cls.__data_to_image(data, width, height))
        pdf.close()
        return page_images

    @staticmethod
    def __data_to_image(data: bytes, width: int, height: int) -> numpy.ndarray:
        """二进制字节数组转cv2图片"""
        # 将字节数组转为np格式数据
        numpy_data = numpy.frombuffer(data, numpy.uint8)
        # bmp格式数据转图片
        if len(numpy_data) % (width * height) == 0:
            return numpy.reshape(numpy_data, (height, width, len(numpy_data) // (width * height)))
        # jpg或png格式转图片
        return cv2.imdecode(numpy_data, cv2.IMREAD_ANYCOLOR)

    @staticmethod
    def __recover_pix(pdf: fitz.Document, item: tuple) -> typing.Union[dict, fitz.Pixmap]:
        """Return image for a given XREF."""
        x = item[0]  # xref of PDF image
        s = item[1]  # xref of its /SMask
        if s == 0:  # no SMask: use direct image output
            return pdf.extract_image(x)

        # we need to reconstruct the alpha channel with the SMask
        pix_x = fitz.Pixmap(pdf, x)  # create pixmap of the PDF entry
        pix_s = fitz.Pixmap(pdf, s)  # create pixmap of the SMask entry

        """Sanity check:
        - both pix_maps must have the same rectangle
        - both pix_maps must have alpha=0
        - pix_s must consist of 1 byte per pixel
        """

        def get_image(p: fitz.Pixmap) -> fitz.Pixmap:
            if p.colorspace.n != 4:
                return p
            return fitz.Pixmap(fitz.csRGB, p)

        if not (pix_x.irect == pix_s.irect and pix_x.alpha == pix_s.alpha == 0 and pix_s.n == 1):
            # logging.warning(f"unsupported /SMask {s} for {x}: {pix_s}")
            return get_image(pix_x)  # return the pixmap as is

        pix = fitz.Pixmap(pix_x)  # copy of pix_x, with an alpha channel added
        pix.set_alpha(pix_s.samples)  # treat pix_s.samples as the alpha values
        # we may need to adjust something for CMYK pix_maps here:
        return get_image(pix)
