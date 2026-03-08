"""RAG Pipeline — orchestrates the full Retrieval-Augmented Generation flow."""

import uuid
import logging
from typing import Dict, List, Optional
from app.optimizer.router import router as cost_router
from app.core.vector_store import vector_store
from app.core.chunker import chunk_text
from app.utils.file_parser import parse_file

logger = logging.getLogger("budai.rag")

# Budai (布袋) — Compassionate AI Personality
RAG_SYSTEM_PROMPT = """Bạn là budAI 布袋 — trợ lý AI mang hình tượng Bố Đại Hòa Thượng (Laughing Buddha).

🪷 TÍNH CÁCH BỐ ĐẠI:
- Từ bi, nhẹ nhàng, luôn tươi cười như Phật Di Lặc
- Mang túi vải chứa tri thức, cho đi không giữ lại
- Trí tuệ sâu sắc nhưng lời nói giản dị, ai cũng hiểu
- Không phán xét, không tranh cãi — chỉ soi sáng
- Hài hước nhẹ nhàng khi phù hợp

📖 NGUYÊN TẮC TRẢ LỜI:
- Trả lời dựa trên ngữ cảnh/tài liệu được cung cấp
- Nếu không đủ thông tin → nói thật, khuyên tìm thêm
- Trích dẫn nguồn khi có thể [1], [2]...
- Trả lời bằng ngôn ngữ của câu hỏi (VN, EN, Myanmar, Khmer...)
- Với câu hỏi Phật pháp → giải thích ý nghĩa sâu, liên hệ thực tế
- Kết thúc bằng 1 câu khích lệ nhẹ nhàng khi phù hợp

Bố Đại cười nói: "Mở túi vải ra, có gì cho hết!" 🪷"""

RAG_PROMPT_TEMPLATE = """Ngữ cảnh tham khảo:
---
{context}
---

Câu hỏi: {question}

Hãy trả lời dựa trên ngữ cảnh trên:"""


class RAGPipeline:
    """Full RAG pipeline: ingest → embed → store → query → generate."""

    async def ingest_file(
        self,
        filename: str,
        content_bytes: bytes,
        collection: str = None,
        chunk_size: int = None,
        chunk_overlap: int = None,
        strategy: str = None,
    ) -> Dict:
        """
        Ingest a file: parse → chunk → embed → store.

        Returns dict with doc_id, chunk_count, cost, etc.
        """
        doc_id = str(uuid.uuid4())[:8]

        # 1. Parse file
        text = parse_file(filename, content_bytes)
        if not text.strip():
            raise ValueError(f"Could not extract text from '{filename}'")

        # 2. Chunk
        chunks = chunk_text(text, chunk_size, chunk_overlap)
        if not chunks:
            raise ValueError(f"No chunks produced from '{filename}'")

        # 3. Embed via cheapest provider
        embed_result = await cost_router.embed(chunks, strategy=strategy)

        # 4. Store in vector DB
        metadata = {"filename": filename, "source": filename}
        stored = vector_store.add_documents(
            chunks=chunks,
            embeddings=embed_result.embeddings,
            doc_id=doc_id,
            metadata=metadata,
            collection=collection,
        )

        result = {
            "doc_id": doc_id,
            "filename": filename,
            "text_length": len(text),
            "chunk_count": len(chunks),
            "embedding_provider": embed_result.provider,
            "embedding_model": embed_result.model,
            "embedding_tokens": embed_result.token_count,
            "embedding_cost_usd": embed_result.cost_usd,
        }
        logger.info(f"📥 Ingested '{filename}' → {len(chunks)} chunks, ${embed_result.cost_usd:.6f}")
        return result

    async def query(
        self,
        question: str,
        collection: str = None,
        top_k: int = None,
        strategy: str = None,
        provider: str = None,
        model: str = None,
        max_tokens: int = 2048,
    ) -> Dict:
        """
        Full RAG query: embed question → search → generate answer.

        Returns dict with answer, sources, cost, etc.
        """
        # 1. Embed the question
        embed_result = await cost_router.embed([question], strategy=strategy)
        query_embedding = embed_result.embeddings[0]

        # 2. Search vector store
        results = vector_store.query(
            query_embedding=query_embedding,
            top_k=top_k,
            collection=collection,
        )

        if not results:
            return {
                "answer": "Không tìm thấy tài liệu liên quan. Vui lòng upload tài liệu trước.",
                "sources": [],
                "cost": {"embedding": embed_result.cost_usd, "generation": 0, "total": embed_result.cost_usd},
            }

        # 3. Build context from retrieved docs
        context_parts = []
        sources = []
        for i, doc in enumerate(results):
            context_parts.append(f"[{i+1}] {doc['text']}")
            sources.append({
                "chunk": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"],
                "metadata": doc["metadata"],
                "relevance_score": 1 - doc["distance"],  # cosine distance → similarity
            })

        context = "\n\n".join(context_parts)
        prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

        # 4. Generate answer via cheapest provider
        gen_result = await cost_router.generate(
            prompt=prompt,
            system_prompt=RAG_SYSTEM_PROMPT,
            strategy=strategy,
            provider=provider,
            model=model,
            max_tokens=max_tokens,
        )

        total_cost = embed_result.cost_usd + gen_result.cost_usd

        return {
            "answer": gen_result.text,
            "sources": sources,
            "model": {
                "embedding": f"{embed_result.provider}/{embed_result.model}",
                "generation": f"{gen_result.provider}/{gen_result.model}",
            },
            "tokens": {
                "embedding": embed_result.token_count,
                "generation_input": gen_result.input_tokens,
                "generation_output": gen_result.output_tokens,
            },
            "cost": {
                "embedding_usd": embed_result.cost_usd,
                "generation_usd": gen_result.cost_usd,
                "total_usd": total_cost,
            },
        }

    async def embed_only(
        self,
        texts: List[str],
        strategy: str = None,
        provider: str = None,
        model: str = None,
    ) -> Dict:
        """Generate embeddings without storing them."""
        result = await cost_router.embed(
            texts, strategy=strategy, provider=provider, model=model
        )
        return {
            "embeddings": result.embeddings,
            "provider": result.provider,
            "model": result.model,
            "token_count": result.token_count,
            "cost_usd": result.cost_usd,
        }


# Singleton
rag = RAGPipeline()
