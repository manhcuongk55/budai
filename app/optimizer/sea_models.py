"""
SEA Language Model Registry — Best AI models for Southeast Asian languages.
Covers: Vietnamese 🇻🇳, Myanmar 🇲🇲, Khmer 🇰🇭, Lao 🇱🇦, Tetum 🇹🇱
"""

# ═══════════════════════════════════════════════════════
#  OCR MODELS — Optical Character Recognition
# ═══════════════════════════════════════════════════════
OCR_MODELS = {
    "paddleocr-vl": {
        "name": "PaddleOCR-VL",
        "params": "0.9B",
        "languages": 109,
        "supports": ["vi", "my", "km", "lo", "th", "zh", "ja", "ko", "en"],
        "features": ["text", "tables", "formulas", "complex_layouts"],
        "license": "Apache-2.0",
        "cost": "free (self-hosted)",
        "quality": 0.90,
        "url": "https://github.com/PaddlePaddle/PaddleOCR",
        "notes": "Best overall multilingual OCR. Supports complex scripts.",
    },
    "dots-ocr": {
        "name": "dots.ocr",
        "params": "1.7B",
        "languages": 100,
        "supports": ["vi", "my", "km", "lo", "th", "en"],
        "features": ["layout_detection", "content_recognition", "low_resource"],
        "license": "MIT",
        "cost": "free (self-hosted)",
        "quality": 0.92,
        "url": "https://github.com/nicholasruunu/dots.ocr",
        "notes": "SOTA 2025. Best for low-resource SEA languages.",
    },
    "deepseek-ocr": {
        "name": "DeepSeek OCR",
        "params": "varies",
        "languages": 100,
        "supports": ["vi", "my", "km", "lo", "th", "zh", "en"],
        "features": ["pdf_parsing", "complex_layouts", "scientific"],
        "license": "MIT",
        "cost": "free (self-hosted) or API",
        "quality": 0.88,
        "url": "https://platform.deepseek.com",
        "notes": "Trained on 30M+ PDF pages. Good for documents.",
    },
    "easyocr": {
        "name": "EasyOCR",
        "params": "small",
        "languages": 80,
        "supports": ["vi", "my", "km", "lo", "th", "en"],
        "features": ["easy_setup", "numbers", "python_native"],
        "license": "Apache-2.0",
        "cost": "free",
        "quality": 0.75,
        "url": "https://github.com/JaidedAI/EasyOCR",
        "notes": "Easiest to integrate. Good for quick prototyping.",
    },
    "tesseract": {
        "name": "Tesseract OCR",
        "params": "small",
        "languages": 100,
        "supports": ["vi", "my", "km", "lo", "th", "en"],
        "features": ["mature", "widely_used", "trainable"],
        "license": "Apache-2.0",
        "cost": "free",
        "quality": 0.65,
        "url": "https://github.com/tesseract-ocr/tesseract",
        "notes": "Needs fine-tuning for complex scripts (Myanmar, Khmer).",
    },
    "surya": {
        "name": "Surya OCR",
        "params": "varies",
        "languages": 90,
        "supports": ["vi", "my", "km", "lo", "th", "en"],
        "features": ["layout_analysis", "tables", "multi_column"],
        "license": "GPL-3.0",
        "cost": "free",
        "quality": 0.85,
        "url": "https://github.com/VikParuchuri/surya",
        "notes": "Great for complex document layouts.",
    },
    "myocr": {
        "name": "myOCR (Myanmar specific)",
        "params": "small",
        "languages": 1,
        "supports": ["my"],
        "features": ["myanmar_specialized", "synthetic_dataset"],
        "license": "open-source",
        "cost": "free",
        "quality": 0.80,
        "url": "https://github.com/myOCR",
        "notes": "Specialized for Myanmar/Burmese. Best accuracy for Myanmar.",
    },
}


# ═══════════════════════════════════════════════════════
#  TTS MODELS — Text-to-Speech
# ═══════════════════════════════════════════════════════
TTS_MODELS = {
    "mms-tts-mya": {
        "name": "Facebook MMS TTS Myanmar",
        "architecture": "VITS",
        "language": "my",
        "language_name": "Myanmar (Burmese)",
        "license": "CC-BY-NC",
        "cost": "free (self-hosted)",
        "quality": 0.75,
        "url": "https://huggingface.co/facebook/mms-tts-mya",
    },
    "mms-tts-khm": {
        "name": "Facebook MMS TTS Khmer",
        "architecture": "VITS",
        "language": "km",
        "language_name": "Khmer (Cambodian)",
        "license": "CC-BY-NC",
        "cost": "free (self-hosted)",
        "quality": 0.75,
        "url": "https://huggingface.co/facebook/mms-tts-khm",
    },
    "mms-tts-lao": {
        "name": "Facebook MMS TTS Lao",
        "architecture": "VITS",
        "language": "lo",
        "language_name": "Lao",
        "license": "CC-BY-NC",
        "cost": "free (self-hosted)",
        "quality": 0.75,
        "url": "https://huggingface.co/facebook/mms-tts-lao",
    },
    "xtts-v2": {
        "name": "XTTS-v2 (Coqui AI)",
        "architecture": "Transformer",
        "language": "multilingual",
        "language_name": "23+ languages, voice cloning",
        "license": "MPL-2.0",
        "cost": "free (self-hosted)",
        "quality": 0.90,
        "url": "https://huggingface.co/coqui/XTTS-v2",
        "notes": "Best quality multilingual TTS. Zero-shot voice cloning.",
    },
    "chatterbox": {
        "name": "Chatterbox (Resemble AI)",
        "architecture": "Transformer",
        "language": "multilingual",
        "language_name": "Multi-language + emotion control",
        "license": "MIT",
        "cost": "free (self-hosted)",
        "quality": 0.88,
        "url": "https://github.com/resemble-ai/chatterbox",
        "notes": "Production-grade. Emotion control. Real-time.",
    },
    "melotts": {
        "name": "MeloTTS (MyShell)",
        "architecture": "Transformer",
        "language": "multilingual",
        "language_name": "Multiple languages, CPU optimized",
        "license": "MIT",
        "cost": "free (self-hosted)",
        "quality": 0.82,
        "url": "https://github.com/myshell-ai/MeloTTS",
        "notes": "Real-time on CPU. Very efficient.",
    },
}


# ═══════════════════════════════════════════════════════
#  EMBEDDING MODELS — Best for SEA RAG
# ═══════════════════════════════════════════════════════
SEA_EMBEDDING_MODELS = {
    "bge-m3": {
        "name": "BAAI BGE-M3",
        "languages": 100,
        "supports_sea": True,
        "dim": 1024,
        "max_tokens": 8192,
        "license": "MIT",
        "cost": "free (self-hosted) or API",
        "quality": 0.90,
        "url": "https://huggingface.co/BAAI/bge-m3",
        "notes": "Best for multilingual RAG. Dense + sparse + multi-vector.",
    },
    "jina-v4": {
        "name": "Jina Embeddings v4",
        "languages": 100,
        "supports_sea": True,
        "dim": 1024,
        "max_tokens": 8192,
        "license": "Apache-2.0",
        "cost": "free (self-hosted) or Jina API",
        "quality": 0.88,
        "url": "https://huggingface.co/jinaai/jina-embeddings-v4",
        "notes": "Multimodal + multilingual. Universal retrieval.",
    },
    "cohere-v4": {
        "name": "Cohere Embed v4",
        "languages": 100,
        "supports_sea": True,
        "dim": 1024,
        "max_tokens": 128000,
        "license": "proprietary",
        "cost": "API pricing",
        "quality": 0.92,
        "url": "https://cohere.com/embed",
        "notes": "SOTA multimodal embedding. Great for SEA languages.",
    },
    "snowflake-arctic": {
        "name": "Snowflake Arctic-Embed L v2.0",
        "languages": 74,
        "supports_sea": True,
        "dim": 1024,
        "max_tokens": 8192,
        "license": "Apache-2.0",
        "cost": "free (self-hosted)",
        "quality": 0.85,
        "url": "https://huggingface.co/Snowflake/arctic-embed-l-v2.0",
        "notes": "Production-grade. High retrieval quality.",
    },
}


# ═══════════════════════════════════════════════════════
#  LANGUAGE COVERAGE MATRIX
# ═══════════════════════════════════════════════════════
LANGUAGE_SUPPORT = {
    "vi": {"name": "Vietnamese 🇻🇳", "ocr": "excellent", "tts": "good", "embedding": "excellent"},
    "my": {"name": "Myanmar 🇲🇲", "ocr": "good", "tts": "basic", "embedding": "fair"},
    "km": {"name": "Khmer 🇰🇭", "ocr": "good", "tts": "basic", "embedding": "fair"},
    "lo": {"name": "Lao 🇱🇦", "ocr": "good", "tts": "basic", "embedding": "fair"},
    "tet": {"name": "Tetum 🇹🇱", "ocr": "limited", "tts": "none", "embedding": "limited"},
    "th": {"name": "Thai 🇹🇭", "ocr": "excellent", "tts": "good", "embedding": "good"},
}


def get_models_summary():
    """Get full model summary for API response."""
    return {
        "ocr": {k: {"name": v["name"], "quality": v["quality"], "languages": v.get("languages", 0),
                     "notes": v.get("notes", "")} for k, v in OCR_MODELS.items()},
        "tts": {k: {"name": v["name"], "quality": v["quality"], "language": v.get("language_name", ""),
                     "notes": v.get("notes", "")} for k, v in TTS_MODELS.items()},
        "embedding": {k: {"name": v["name"], "quality": v["quality"], "languages": v["languages"],
                          "notes": v.get("notes", "")} for k, v in SEA_EMBEDDING_MODELS.items()},
        "language_coverage": LANGUAGE_SUPPORT,
    }
