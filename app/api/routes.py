"""API Routes — all budAI endpoints."""

import logging
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from app.api.models import (
    QueryRequest,
    QueryResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    IngestResponse,
    DocumentInfo,
    ErrorResponse,
)
from app.core.rag_pipeline import rag
from app.core.vector_store import vector_store
from app.optimizer.router import router as cost_router
from app.optimizer.pricing import get_pricing_table
from app.optimizer.sea_models import get_models_summary
from app.utils.test_data_loader import download_test_data, get_test_data_info
from app.utils.dharma_data import create_dharma_data, get_dharma_info

logger = logging.getLogger("budai.api")

api_router = APIRouter(prefix="/api/v1", tags=["budAI API"])


# ═══════ Health & Info ═══════

@api_router.get("/health")
async def health_check():
    """Service health + provider status."""
    provider_status = await cost_router.get_status()
    store_stats = vector_store.get_stats()
    return {
        "status": "healthy",
        "service": "budAI",
        "version": "1.0.0",
        "providers": provider_status,
        "vector_store": store_stats,
    }


@api_router.get("/providers")
async def list_providers():
    """List all providers with pricing info."""
    return {
        "available": cost_router.list_providers(),
        "pricing": get_pricing_table(),
    }


@api_router.get("/providers/status")
async def providers_status():
    """Real-time provider health check."""
    return await cost_router.get_status()


# ═══════ Documents ═══════

@api_router.post("/documents/upload", response_model=IngestResponse)
async def upload_document(
    file: UploadFile = File(...),
    collection: Optional[str] = Query(None, description="Collection name"),
    chunk_size: Optional[int] = Query(None, description="Chunk size"),
    chunk_overlap: Optional[int] = Query(None, description="Chunk overlap"),
    strategy: Optional[str] = Query(None, description="cheapest|fastest|best"),
):
    """Upload & ingest a document (PDF, DOCX, TXT, MD)."""
    try:
        content = await file.read()
        result = await rag.ingest_file(
            filename=file.filename,
            content_bytes=content,
            collection=collection,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            strategy=strategy,
        )
        return IngestResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/documents", response_model=List[DocumentInfo])
async def list_documents(
    collection: Optional[str] = Query(None, description="Collection name"),
):
    """List all ingested documents."""
    docs = vector_store.list_documents(collection)
    return [DocumentInfo(**d) for d in docs]


@api_router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    collection: Optional[str] = Query(None, description="Collection name"),
):
    """Delete a document and its chunks."""
    success = vector_store.delete_document(doc_id, collection)
    if success:
        return {"status": "deleted", "doc_id": doc_id}
    raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")


# ═══════ RAG Query ═══════

@api_router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    🙏 RAG Query — Ask a question, get an answer with sources.

    Automatically uses the cheapest provider by default.
    Override with ?strategy=fastest or ?strategy=best.
    """
    try:
        result = await rag.query(
            question=request.question,
            collection=request.collection,
            top_k=request.top_k,
            strategy=request.strategy,
            provider=request.provider,
            model=request.model,
            max_tokens=request.max_tokens,
        )
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════ Embeddings ═══════

@api_router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """Generate embeddings without storing in vector DB."""
    try:
        result = await rag.embed_only(
            texts=request.texts,
            strategy=request.strategy,
            provider=request.provider,
            model=request.model,
        )
        return EmbeddingResponse(**result)
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════ Collections ═══════

@api_router.get("/collections")
async def list_collections():
    """List all vector collections."""
    return {"collections": vector_store.list_collections()}


# ═══════ SEA Language Models ═══════

@api_router.get("/models/sea")
async def sea_models():
    """
    🌏 SEA Language Model Catalog

    Lists recommended OCR, TTS, and Embedding models
    for Southeast Asian languages (VN, Myanmar, Khmer, Lao, Tetum).
    """
    return get_models_summary()


# ═══════ Test Data ═══════

@api_router.get("/test-data")
async def test_data_info():
    """List available test documents."""
    return get_test_data_info()


@api_router.post("/test-data/download")
async def create_test_data():
    """
    📥 Download test documents to server.

    Creates sample documents in Vietnamese, English, Myanmar, Khmer, Lao
    for testing the RAG pipeline.
    """
    try:
        result = await download_test_data()
        return {"status": "success", "documents_created": len(result), "files": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/test-data/ingest")
async def ingest_test_data(
    strategy: Optional[str] = Query(None, description="cheapest|fastest|best"),
):
    """
    📥 Download AND ingest all test documents into vector store.

    This creates test data files, then uploads each one through the RAG pipeline.
    """
    import os

    try:
        # Create test files
        docs = await download_test_data()

        # Ingest each
        results = []
        for doc in docs:
            filepath = os.path.join("./data/test_documents", doc["file"])
            with open(filepath, "rb") as f:
                content = f.read()
            result = await rag.ingest_file(
                filename=doc["file"],
                content_bytes=content,
                strategy=strategy,
            )
            results.append(result)

        total_cost = sum(r["embedding_cost_usd"] for r in results)
        total_chunks = sum(r["chunk_count"] for r in results)

        return {
            "status": "success",
            "documents_ingested": len(results),
            "total_chunks": total_chunks,
            "total_embedding_cost_usd": total_cost,
            "details": results,
        }
    except Exception as e:
        logger.error(f"Test data ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════ Dharma 🪷 ═══════

@api_router.get("/dharma")
async def dharma_info():
    """🪷 List available Buddhist scriptures."""
    return get_dharma_info()


@api_router.post("/dharma/load")
async def load_dharma():
    """
    🪷 Create Dharma scripture files on disk.

    Heart Sutra, Diamond Sutra, Dhammapada (VN, EN, Myanmar, Khmer),
    Four Noble Truths, Meditation Guide, SEA Buddhist History.
    """
    try:
        result = create_dharma_data()
        return {"status": "success", "texts_created": len(result), "files": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/dharma/ingest")
async def ingest_dharma(
    strategy: Optional[str] = Query(None, description="cheapest|fastest|best"),
):
    """
    🪷 Load AND ingest all Dharma scriptures into vector store.

    Upload kinh Phật → Hỏi đáp nghĩa kinh bằng AI.
    """
    import os

    try:
        docs = create_dharma_data()
        results = []
        for doc in docs:
            filepath = os.path.join("./data/dharma", doc["file"])
            with open(filepath, "rb") as f:
                content = f.read()
            result = await rag.ingest_file(
                filename=doc["file"],
                content_bytes=content,
                collection="dharma",
                strategy=strategy,
            )
            results.append(result)

        total_cost = sum(r["embedding_cost_usd"] for r in results)
        total_chunks = sum(r["chunk_count"] for r in results)

        return {
            "status": "success",
            "texts_ingested": len(results),
            "total_chunks": total_chunks,
            "total_embedding_cost_usd": total_cost,
            "collection": "dharma",
            "details": results,
        }
    except Exception as e:
        logger.error(f"Dharma ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
