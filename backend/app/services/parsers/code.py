from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class CodeParser:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def parse(self, content: str, language: str = "python") -> list:
        return self.splitter.split_text(content)


code_parser = CodeParser()
