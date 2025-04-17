from pathlib import pathlib.Path

import pygame

from common_util.file_util.file_util.file_util import FileUtil


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> str:
        file_path = pathlib.Path(__file__).parent.parent.joinpath(f"file/{file_name}")
        FileUtil.make_dir(file_path)
        return str(file_path)

    @classmethod
    def load_font(cls, font_name: str, font_size: int) -> pygame.font.Font:
        """加载字体"""
        return pygame.font.Font(cls.get_file_path(font_name), font_size)

    @classmethod
    def load_image(cls, image_name: str) -> pygame.Surface:
        """获取图片对象"""
        return pygame.image.load(cls.get_file_path(image_name)).convert_alpha()

    @classmethod
    def load_music(cls, music_name: str):
        """加载音乐"""
        pygame.mixer.music.load(cls.get_file_path(music_name))

    @classmethod
    def load_sound(cls, sound_name: str) -> pygame.mixer.Sound:
        """加载音效"""
        return pygame.mixer.Sound(cls.get_file_path(sound_name))
