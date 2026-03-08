"""File Parser — extract text from PDF, DOCX, TXT, MD files."""

import os
import chardet
from typing import Optional


def parse_file(file_path: str, content_bytes: Optional[bytes] = None) -> str:
    """
    Extract text content from a file.

    Args:
        file_path: Path or filename (used to detect extension)
        content_bytes: Raw file bytes (if not provided, reads from file_path)

    Returns:
        Extracted text content
    """
    ext = os.path.splitext(file_path)[1].lower()

    if content_bytes is None:
        with open(file_path, "rb") as f:
            content_bytes = f.read()

    if ext == ".pdf":
        return _parse_pdf(content_bytes)
    elif ext == ".docx":
        return _parse_docx(content_bytes)
    elif ext in (".txt", ".md", ".csv", ".json", ".html", ".xml", ".log"):
        return _parse_text(content_bytes)
    else:
        # Try as text
        return _parse_text(content_bytes)


def _parse_pdf(content: bytes) -> str:
    """Extract text from PDF bytes."""
    from pypdf import PdfReader
    import io

    reader = PdfReader(io.BytesIO(content))
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n\n".join(texts)


def _parse_docx(content: bytes) -> str:
    """Extract text from DOCX bytes."""
    from docx import Document
    import io

    doc = Document(io.BytesIO(content))
    texts = []
    for para in doc.paragraphs:
        if para.text.strip():
            texts.append(para.text)
    return "\n\n".join(texts)


def _parse_text(content: bytes) -> str:
    """Decode text bytes with auto-encoding detection."""
    # Try UTF-8 first
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        pass

    # Auto-detect encoding
    detected = chardet.detect(content)
    encoding = detected.get("encoding", "utf-8") or "utf-8"
    return content.decode(encoding, errors="replace")
