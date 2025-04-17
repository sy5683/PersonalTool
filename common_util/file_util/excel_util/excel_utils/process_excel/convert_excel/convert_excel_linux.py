import typing


class ConvertExcelLinux:

    @staticmethod
    def re_save_excel(excel_path: str):
        """重新保存excel"""
        raise SystemError("Linux系统暂不支持该方法")

    @staticmethod
    def xls_to_xlsx(excel_path: str, save_path: typing.Union[pathlib.Path, str]) -> str:
        """xls文件转换为xlsx文件"""
        raise SystemError("Linux系统暂不支持该方法")

    @staticmethod
    def excel_to_images(excel_path: str, save_path: typing.Union[pathlib.Path, str]) -> typing.List[str]:
        """excel转图片"""
        raise SystemError("Linux系统暂不支持该方法")
