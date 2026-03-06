from typing import List


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    text = " ".join(text.split())  # clean extra whitespace
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # move back a bit to create overlap
        if start < 0:
            start = 0
        if end == len(text):
            break

    return chunks
