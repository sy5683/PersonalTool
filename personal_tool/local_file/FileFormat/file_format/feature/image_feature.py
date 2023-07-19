import os

from PIL import Image


class ImageFeature:

    @staticmethod
    def convert_webp_to_jpg(image_path: str):
        with Image.open(image_path) as image:
            if image.mode == "RGBA":
                image.load()
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
            image_save_path = image_path.replace(".webp", ".jpg")
            image.save(image_save_path)
        os.remove(image_path)
