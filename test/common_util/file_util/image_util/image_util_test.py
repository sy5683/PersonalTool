from common_core.base.test_base import TestBase
from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.image_util.image_util import ImageUtil


class ImageUtilTestCase(TestBase):

    def setUp(self):
        self.image_path = self.get_test_file("测试.png")
        self.save_image_path = self.get_test_file("测试保存.bmp")
        self.template_image_path = self.get_test_file("测试模板.bmp")

    def test_convert_to_jpg_by_opencv(self):
        jpg_path = ImageUtil.convert_to_jpg_by_opencv(self.image_path)
        print(jpg_path)

    def test_convert_to_jpg_by_pil(self):
        jpg_path = ImageUtil.convert_to_jpg_by_pil(self.image_path)
        print(jpg_path)

    def test_get_image_pos(self):
        x, y = ImageUtil.get_image_pos(self.template_image_path)
        print(x, y)

    def test_re_scale(self):
        new_size = (210, 297)  # A4宽高比
        image_path = ImageUtil.re_scale(self.image_path, new_size, self.save_image_path)
        print(image_path)

    def test_rotate_image(self):
        image = ImageUtil.read_opencv_image(self.image_path)
        rotate_image = ImageUtil.rotate_image(image, 45)
        ImageUtil.save_opencv_image(rotate_image, self.save_image_path)

    def test_screenshot(self):
        image_paths = ImageUtil.screenshot(self.save_image_path)
        for image_path in image_paths:
            Win32Util.open_file(image_path)
