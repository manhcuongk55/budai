# budAI 布袋 — AI cười tươi, giá nhân từ

> *Mang túi vải chứa tri thức, cho đi không giữ lại*

<img src="static/budai_logo.png" width="100" alt="budAI">

## 🪷 Giới thiệu

**budAI** (布袋 AI) — Platform RAG thông minh với tối ưu chi phí AI, hỗ trợ đa ngôn ngữ Đông Nam Á.

- 📄 Upload tài liệu → Chat hỏi đáp với AI
- 💰 Tự động route provider rẻ nhất
- 🪷 Kinh Phật tích hợp sẵn (Dharma RAG)
- 🌏 Hỗ trợ 🇻🇳🇲🇲🇰🇭🇱🇦🇹🇱 OCR, TTS

## ⚡ Chạy nhanh

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
# → Mở http://localhost:8000
```

## 🔑 API Keys (miễn phí)

Tạo file `.env`:
```
GOOGLE_API_KEY=...      # free tại aistudio.google.com
GROQ_API_KEY=...        # free tại console.groq.com
OPENROUTER_API_KEY=...  # free tại openrouter.ai
```

Không cần API key cũng chạy được (dùng HuggingFace free).

## 📖 API Endpoints

| Endpoint | Mô tả |
|----------|-------|
| `GET /` | Web product UI |
| `GET /api/v1/health` | Health check |
| `POST /api/v1/documents/upload` | Upload & ingest tài liệu |
| `POST /api/v1/query` | RAG query |
| `POST /api/v1/dharma/ingest` | Nạp kinh Phật |
| `GET /api/v1/models/sea` | Catalog model ĐNÁ |
| `GET /docs` | Swagger API docs |

## 🏗 Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Vector DB**: ChromaDB
- **Embedding**: HuggingFace (free), OpenAI, Google
- **LLM**: Groq, DeepSeek, OpenRouter (free models)
- **Frontend**: Vanilla HTML/CSS/JS
- **Deploy**: Vercel / Docker

## 🪷 Triết lý

Lấy cảm hứng từ **Bố Đại Hòa Thượng** (布袋和尚) — vị tăng cười tươi, mang túi vải lớn chứa đầy vật phẩm, cho đi không giữ lại. budAI mang tinh thần ấy vào thế giới AI: **từ bi, hào phóng, và luôn tươi cười**.

---

*budAI 🪷 — AI cười tươi, giá nhân từ*
