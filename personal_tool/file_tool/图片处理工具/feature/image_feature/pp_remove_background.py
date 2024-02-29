import typing
from pathlib import Path

import cv2
import numpy
import onnxruntime

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from .image_feature import ImageFeature


class PPRemoveBackground:

    @classmethod
    def matting_picture(cls, file_paths: typing.List[str], background_color: typing.Tuple[int, int, int] = None):
        """抠取图像"""
        # 获取pp模型
        model_path = Path(__file__).parent.parent.parent.joinpath("file\\ppseg\\ppseg.onnx")
        session = onnxruntime.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        input_name = session.get_inputs()[0].name
        # 处理图片
        image_paths = ImageFeature.to_image_paths(file_paths)
        for image_path in image_paths:
            image = ImageUtil.read_opencv_image(image_path)
            # 对原图进行resize操作，图片大小必须为32的倍数
            image = cls.__resize_image(image, short=32)
            # 进行归一化
            input_image = cls.__normalize_image(image)
            # 使用pp模型替换背景
            prediction = session.run(None, {input_name: input_image})
            prediction = numpy.squeeze(prediction)
            prediction = cv2.resize(prediction, image.shape[:2][::-1], interpolation=cv2.INTER_LINEAR)
            if background_color is None:
                prediction = prediction[:, :, None]
                prediction = (prediction * 255).astype(numpy.uint8)
                cutout = numpy.concatenate((image, prediction), axis=-1)
                save_path = FileUtil.get_temp_path(f"{Path(image_path).stem}.png")  # 透明图片必须保存为png
            else:
                prediction = cv2.cvtColor(prediction, cv2.COLOR_GRAY2BGR)
                background_color = numpy.asarray(background_color, dtype=numpy.uint8)
                cutout = (background_color * (1 - prediction) + image * prediction).astype(numpy.uint8)
                save_path = FileUtil.get_temp_path(Path(image_path).name)
            ImageUtil.save_opencv_image(cutout, save_path)
        Win32Util.open_file(FileUtil.get_temp_path())

    @staticmethod
    def __resize_image(image: numpy.ndarray, short: int = 32) -> numpy.ndarray:
        """将图片等比处理为需要的大小"""
        short_edge = min(image.shape[:2])
        scale = 1 if short_edge > short else short / short_edge
        width_and_height = numpy.asarray(image.shape)[:2][::-1]
        width_and_height = (width_and_height * scale).astype(int) // short * short
        return cv2.resize(image, width_and_height, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def __normalize_image(image: numpy.ndarray) -> numpy.ndarray:
        """图片归一化"""
        tmp_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im_ary = (tmp_img / 255 - (0.5, 0.5, 0.5)) / (0.5, 0.5, 0.5)
        tmp_img = im_ary.transpose((2, 0, 1))
        return numpy.expand_dims(tmp_img, 0).astype(numpy.float32)
