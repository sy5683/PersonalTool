import logging
import re
import shutil
import typing
import zipfile

import magic
import py7zr
import rarfile


class Decompress:

    @classmethod
    def decompress(cls, file_path: pathlib.Path, password: str) -> typing.Generator[pathlib.Path, None, None]:
        """解压文件，可以传入压缩文件或者存放多个压缩文件的文件夹"""
        logging.info(f"解压文件: {file_path}")
        zip_paths = file_path.glob("*.*") if file_path.is_dir() else [file_path]
        for zip_path in zip_paths:
            save_path = cls.__to_save_path(zip_path)
            if save_path.is_dir():
                shutil.rmtree(save_path)
            cls._decompress_all(zip_path, password)
            yield save_path

    @classmethod
    def _decompress_all(cls, zip_path: pathlib.Path, password: str):
        """递归解压缩压缩文件中的所有文件"""
        # 1) 解压压缩包
        if zip_path.is_file():
            # 1.1) 根据文件读取出来的二进制数据开头判断文件类型
            with open(zip_path, "rb") as file:
                file_type = magic.Magic().from_buffer(file.read(1024))
            # 1.2) 生成解压文件路径
            save_path = cls.__to_save_path(zip_path)
            while save_path.exists():
                save_path = zip_path.parent.joinpath(f"{save_path.name}~")
            # 1.3) 根据文件类型使用对应的方法解压文件
            if re.search("7-zip archive data", file_type):
                cls._decompress_7z(zip_path, save_path, password)
            elif re.search("RAR archive data", file_type):
                cls._decompress_rar(zip_path, save_path, password)
            elif re.search("Zip archive data", file_type):
                cls._decompress_zip(zip_path, save_path, password)
            # 2.1) 解压完成后的文件可能因为格式原因出现乱码，格式化一下
            if save_path.is_dir():
                cls.__format_decompress_file(save_path)
                # 2.2) 遍历解压出来的文件，递归解压被解压出来的文件
                for zip_path in save_path.glob("*"):
                    cls._decompress_all(zip_path, password)
        # 3) 递归遍历解压压缩包
        else:
            zip_paths = list(zip_path.glob("*"))
            # 待解压文件超过一定数量则一般说明解压完成，如果出现特殊情况也属于超大型压缩包，手动解压更好
            if len(zip_paths) > 10:
                logging.info(f"解压完成: {zip_path}")
                return
            for zip_path in zip_paths:
                cls._decompress_all(zip_path, password)

    @classmethod
    def _decompress_7z(cls, zip_path: pathlib.Path, save_path: pathlib.Path, password: str):
        """解压7z文件"""
        logging.info(f"解压7z文件: {zip_path}")
        # 1) 判断压缩包是否分卷
        if re.search(r"\.7z\.001$", str(zip_path)):  # 7z的分卷规则是: .7z后面跟分卷编号
            zip_path = cls.__merge_zip_by_7z(zip_path)
        # 2) 解压7z文件
        try:
            with py7zr.SevenZipFile(zip_path, password=password) as zip_file:
                zip_file.extractall(save_path)
        except py7zr.exceptions.Bad7zFile:
            logging.warning(f"解压7z文件失败: {zip_path}")
        except py7zr.exceptions.PasswordRequired:
            logging.warning(f"7z文件需要密码: {zip_path}")

    @classmethod
    def _decompress_rar(cls, zip_path: pathlib.Path, save_path: pathlib.Path, password: str):
        """解压rar文件"""
        logging.info(f"解压rar文件: {zip_path}")
        rarfile.UNRAR_TOOL = str(pathlib.Path(__file__).parent.joinpath("UnRAR.exe"))
        with rarfile.RarFile(zip_path) as zip_file:
            zip_file.setpassword(password)
            zip_file.extractall(path=save_path)

    @classmethod
    def _decompress_zip(cls, zip_path: pathlib.Path, save_path: pathlib.Path, password: typing.Union[bytes, str]):
        """解压zip文件"""
        if isinstance(password, str):
            password = password.encode("utf-8")
        logging.info(f"解压zip文件: {zip_path}")
        # 1) 判断压缩包是否分卷
        if re.search(r"\.zip\.001$", str(zip_path)):  # 7z的分卷规则是: .zip后面跟分卷编号
            zip_path = cls.__merge_zip_by_7z(zip_path)
        # 2) 解压zip文件
        with zipfile.ZipFile(zip_path) as zip_file:
            zip_file.extractall(save_path, pwd=password)

    @staticmethod
    def __format_decompress_file(save_path: pathlib.Path):
        """解压完成后的文件可能因为格式原因出现乱码，格式化一下"""
        for file_path in save_path.rglob("*"):
            try:
                file_name = file_path.name.encode("cp437").decode("GBK")
                file_path.rename(file_path.parent.joinpath(file_name))
            except UnicodeEncodeError:
                pass

    @staticmethod
    def __merge_zip_by_7z(zip_path: pathlib.Path) -> pathlib.Path:
        """合并使用7z软件分卷的压缩包"""
        logging.info(f"合并使用7z软件分卷的压缩包: {zip_path.name}")
        contents = b""
        for zip_path in list(zip_path.parent.glob(f"{zip_path.stem}.*")):
            with open(zip_path, "rb") as file:
                contents += file.read()
        new_zip_path = zip_path.parent.joinpath(zip_path.stem)
        with open(new_zip_path, "wb") as file:
            file.write(contents)
        return new_zip_path

    @staticmethod
    def __to_save_path(zip_path: pathlib.Path) -> pathlib.Path:
        save_name = zip_path.name[:zip_path.name.find(".")]
        return zip_path.parent.joinpath(save_name)
