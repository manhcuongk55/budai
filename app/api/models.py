"""API Models — Pydantic schemas for requests and responses."""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


# ═══════ Request Models ═══════

class QueryRequest(BaseModel):
    """RAG query request."""
    question: str = Field(..., description="Câu hỏi cần trả lời", min_length=1)
    collection: Optional[str] = Field(None, description="Vector collection name")
    top_k: Optional[int] = Field(None, description="Số tài liệu tham khảo", ge=1, le=20)
    strategy: Optional[str] = Field(None, description="cheapest | fastest | best")
    provider: Optional[str] = Field(None, description="Force specific provider")
    model: Optional[str] = Field(None, description="Force specific model")
    max_tokens: int = Field(2048, description="Max tokens for answer", ge=1, le=16384)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Hợp đồng thuê nhà có thời hạn bao lâu?",
                    "strategy": "cheapest",
                    "top_k": 5,
                }
            ]
        }
    }


class EmbeddingRequest(BaseModel):
    """Embedding-only request."""
    texts: List[str] = Field(..., description="Texts to embed", min_length=1)
    strategy: Optional[str] = Field(None, description="cheapest | fastest | best")
    provider: Optional[str] = Field(None, description="Force specific provider")
    model: Optional[str] = Field(None, description="Force specific model")


# ═══════ Response Models ═══════

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str
    providers: Dict[str, dict]
    vector_store: Dict


class IngestResponse(BaseModel):
    """Document ingestion response."""
    doc_id: str
    filename: str
    text_length: int
    chunk_count: int
    embedding_provider: str
    embedding_model: str
    embedding_tokens: int
    embedding_cost_usd: float


class QueryResponse(BaseModel):
    """RAG query response."""
    answer: str
    sources: List[Dict]
    model: Dict[str, str]
    tokens: Dict[str, int]
    cost: Dict[str, float]


class EmbeddingResponse(BaseModel):
    """Embedding response."""
    embeddings: List[List[float]]
    provider: str
    model: str
    token_count: int
    cost_usd: float


class DocumentInfo(BaseModel):
    """Document info."""
    doc_id: str
    filename: str
    chunk_count: int


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
