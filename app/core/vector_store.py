"""Vector Store — ChromaDB integration for document storage & retrieval."""

import os
import uuid
import logging
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

logger = logging.getLogger("budai.vectorstore")


class VectorStore:
    """ChromaDB-backed vector store for RAG."""

    def __init__(self, persist_dir: str = None):
        persist_dir = persist_dir or settings.chroma_persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.default_collection = "budai_docs"
        logger.info(f"🗄️  ChromaDB initialized at {persist_dir}")

    def get_or_create_collection(self, name: str = None):
        """Get or create a collection."""
        name = name or self.default_collection
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        doc_id: str,
        metadata: Optional[Dict] = None,
        collection: str = None,
    ) -> int:
        """
        Add document chunks with embeddings to the store.

        Returns:
            Number of chunks added
        """
        col = self.get_or_create_collection(collection)

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "doc_id": doc_id,
                "chunk_index": i,
                **(metadata or {}),
            }
            for i in range(len(chunks))
        ]

        col.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )

        logger.info(f"📄 Added {len(chunks)} chunks for doc '{doc_id}'")
        return len(chunks)

    def query(
        self,
        query_embedding: List[float],
        top_k: int = None,
        collection: str = None,
        where: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search for similar documents.

        Returns:
            List of {text, metadata, distance} dicts
        """
        top_k = top_k or settings.top_k
        col = self.get_or_create_collection(collection)

        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
        }
        if where:
            kwargs["where"] = where

        results = col.query(**kwargs)

        documents = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return documents

    def delete_document(self, doc_id: str, collection: str = None) -> bool:
        """Delete all chunks for a document."""
        col = self.get_or_create_collection(collection)
        try:
            col.delete(where={"doc_id": doc_id})
            logger.info(f"🗑️  Deleted doc '{doc_id}'")
            return True
        except Exception as e:
            logger.error(f"Failed to delete doc '{doc_id}': {e}")
            return False

    def list_documents(self, collection: str = None) -> List[Dict]:
        """List all unique documents in a collection."""
        col = self.get_or_create_collection(collection)
        all_data = col.get()

        docs = {}
        if all_data["metadatas"]:
            for meta in all_data["metadatas"]:
                doc_id = meta.get("doc_id", "unknown")
                if doc_id not in docs:
                    docs[doc_id] = {
                        "doc_id": doc_id,
                        "filename": meta.get("filename", ""),
                        "chunk_count": 0,
                    }
                docs[doc_id]["chunk_count"] += 1

        return list(docs.values())

    def list_collections(self) -> List[str]:
        """List all collections."""
        return [c.name for c in self.client.list_collections()]

    def get_stats(self) -> Dict:
        """Get store statistics."""
        collections = self.client.list_collections()
        stats = {"total_collections": len(collections), "collections": {}}
        for col in collections:
            c = self.client.get_collection(col.name)
            stats["collections"][col.name] = {"count": c.count()}
        return stats


# Singleton instance
vector_store = VectorStore()
