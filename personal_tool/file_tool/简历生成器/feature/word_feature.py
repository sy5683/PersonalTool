import docx


class WordFeature:
    __document = None

    @classmethod
    def get_document(cls) -> docx.Document:
        if cls.__document is None:
            cls.__document = docx.Document()
        return cls.__document

    @classmethod
    def save_document(cls, save_path: str):
        if cls.__document:
            cls.__document.save(save_path)
            cls.__document = None
