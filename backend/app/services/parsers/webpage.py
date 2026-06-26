from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class WebpageParser:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def parse(self, html_content: str) -> list:
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return self.splitter.split_text(text)


webpage_parser = WebpageParser()
