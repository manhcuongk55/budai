"""Document Chunker — split documents into optimal chunks for RAG."""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings


def chunk_text(
    text: str,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List[str]:
    """
    Split text into chunks for embedding.

    Args:
        text: Full document text
        chunk_size: Max characters per chunk (default from config)
        chunk_overlap: Overlap between chunks (default from config)

    Returns:
        List of text chunks
    """
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap or settings.chunk_overlap

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)
    return [c.strip() for c in chunks if c.strip()]
