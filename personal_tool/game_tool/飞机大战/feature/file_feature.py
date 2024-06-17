from pathlib import Path

import pygame

from common_util.file_util.file_util.file_util import FileUtil


class FileFeature:
    _font_map = {}
    _image_map = {}

    @staticmethod
    def get_file_path(file_name: str = '') -> str:
        file_dir_path = Path(__file__).parent.parent.joinpath("file")
        FileUtil.make_dir(file_dir_path)
        return str(file_dir_path.joinpath(file_name))

    @classmethod
    def get_font(cls, font_name: str, font_size: int) -> pygame.font.Font:
        """获取字体"""
        font_key = f"[{font_size}]{font_name}"
        if font_key not in cls._font_map:
            cls._font_map[font_key] = pygame.font.Font(cls.get_file_path(font_name), font_size)
        return cls._font_map[font_key]

    @classmethod
    def get_image(cls, image_name: str) -> pygame.Surface:
        """获取图片对象"""
        if image_name not in cls._image_map:
            cls._image_map[image_name] = pygame.image.load(cls.get_file_path(image_name)).convert_alpha()
        return cls._image_map[image_name]

    @classmethod
    def load_music(cls, music_name: str):
        """加载音乐"""
        pygame.mixer.music.load(cls.get_file_path(music_name))

    @classmethod
    def load_sound(cls, sound_name: str) -> pygame.mixer.Sound:
        """加载音效"""
        return pygame.mixer.Sound(cls.get_file_path(sound_name))
