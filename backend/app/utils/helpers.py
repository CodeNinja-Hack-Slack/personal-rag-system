import re
from typing import List


def extract_code_blocks(text: str) -> List[dict]:
    pattern = r"```(\w+)?\n(.*?)```"
    blocks = []
    for match in re.finditer(pattern, text, re.DOTALL):
        blocks.append({
            "language": match.group(1) or "text",
            "code": match.group(2).strip()
        })
    return blocks


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def generate_title(content: str, max_length: int = 50) -> str:
    first_line = content.split("\n")[0].strip()
    first_line = re.sub(r"^#+\s*", "", first_line)
    if len(first_line) > max_length:
        return first_line[:max_length] + "..."
    return first_line or "Untitled"


def validate_content_type(content_type: str) -> bool:
    valid_types = {"markdown", "code", "webpage", "manual"}
    return content_type in valid_types


def chunk_list(lst: list, chunk_size: int) -> list:
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
