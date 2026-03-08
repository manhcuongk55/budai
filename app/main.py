"""
budAI 🙏 — AI từ bi như Phật Tổ
Smart RAG API with cost optimization.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import api_router
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s 🙏 %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("budai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown."""
    logger.info("═" * 50)
    logger.info("🙏 budAI is awakening...")
    logger.info("   AI từ bi như Phật Tổ")
    logger.info(f"   Strategy: {settings.default_strategy}")
    logger.info("═" * 50)
    yield
    logger.info("🙏 budAI rests in peace...")


app = FastAPI(
    title="budAI 🙏",
    description="""
## AI từ bi như Phật Tổ — Smart RAG API

**budAI** là một RAG API Gateway thông minh, tự động tối ưu chi phí bằng cách
route request đến provider AI rẻ nhất.

### ✨ Tính năng chính
- 📄 **Document Ingestion** — Upload PDF, DOCX, TXT → tự động chunk & embed
- 🔍 **RAG Query** — Tìm tài liệu liên quan + sinh câu trả lời bằng AI
- 💰 **Cost Optimizer** — Tự động chọn provider rẻ nhất (DeepSeek, Gemini, OpenAI...)
- 🔄 **Auto-failover** — Provider nào down thì tự chuyển sang cái khác
- 📊 **Cost Tracking** — Theo dõi chi phí mỗi request

### 🎯 Routing Strategies
- `cheapest` — Rẻ nhất (default)
- `fastest` — Nhanh nhất
- `best` — Chất lượng cao nhất
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router)

# Serve static landing page
import os
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Serve landing page or redirect to docs."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "service": "budAI 🙏",
        "tagline": "AI từ bi như Phật Tổ",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
