from langchain_text_splitters import MarkdownTextSplitter
from app.core.config import settings


class MarkdownParser:
    def __init__(self):
        self.splitter = MarkdownTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def parse(self, content: str) -> list:
        return self.splitter.split_text(content)


markdown_parser = MarkdownParser()
