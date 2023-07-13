import docx


class WordFeature:
    _document = None

    @classmethod
    def get_document(cls) -> docx.Document:
        if cls._document is None:
            cls._document = docx.Document()
        return cls._document

    @classmethod
    def save_document(cls, save_path: str):
        if cls._document:
            cls._document.save(save_path)
            cls._document = None
