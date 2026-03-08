# budAI — Bảng Giá Dịch Vụ Enterprise 🙏

> **Bán giải pháp trọn gói**: Model + Source Code + Triển khai on-premise
> **Không bán API** — Khách hàng sở hữu toàn bộ, tự vận hành

---

## 1. Gói Sản Phẩm

### 🥉 Gói BASIC — RAG API Gateway
| Hạng mục | Chi tiết |
|----------|---------|
| Source code | budAI full source (FastAPI, Docker) |
| Tính năng | RAG pipeline, cost optimizer, multi-provider |
| Models | Dùng API bên ngoài (OpenAI, Google, DeepSeek) |
| Ngôn ngữ | VN, EN + 100 ngôn ngữ |
| Hạ tầng cần | 1 VPS 4 CPU / 8GB RAM (không cần GPU) |
| Bảo trì | 3 tháng hotfix |
| **Giá** | **$5,000 - $8,000** (một lần) |
| Chi phí vận hành | ~$20-100/tháng (API calls) |

---

### 🥈 Gói PRO — Self-hosted AI
| Hạng mục | Chi tiết |
|----------|---------|
| Tất cả gói Basic | ✅ |
| Self-hosted LLM | Qwen2.5-7B hoặc Llama 3.3 |
| Self-hosted Embedding | BGE-M3 / Jina v4 |
| OCR Engine | PaddleOCR-VL (109 ngôn ngữ) |
| Fully offline | Không cần internet, data không rò rỉ |
| Hạ tầng cần | 1 GPU server (A40/L40/RTX 4090, 24GB+ VRAM) |
| Training/Fine-tune | Hướng dẫn fine-tune trên data khách hàng |
| Bảo trì | 6 tháng |
| **Giá** | **$15,000 - $25,000** (một lần) |
| Chi phí vận hành | ~$200-400/tháng (GPU cloud) hoặc $0 nếu có GPU riêng |

---

### 🥇 Gói ENTERPRISE — Full Suite SEA Languages
| Hạng mục | Chi tiết |
|----------|---------|
| Tất cả gói Pro | ✅ |
| OCR đa ngôn ngữ ĐNÁ | VN 🇻🇳, Myanmar 🇲🇲, Khmer 🇰🇭, Lao 🇱🇦, Tetum 🇹🇱 |
| TTS đa ngôn ngữ | Facebook MMS (Myanmar, Khmer, Lao) + XTTS-v2 |
| Custom model training | Fine-tune trên data và domain khách hàng |
| Multi-tenant | Nhiều department dùng chung, phân quyền |
| Dashboard monitoring | Theo dõi usage, chi phí, chất lượng |
| SLA | 99.5% uptime, response < 3s |
| Bảo trì | 12 tháng + ưu tiên hỗ trợ |
| **Giá** | **$40,000 - $80,000** (một lần) |
| Chi phí vận hành | ~$500-1,500/tháng (GPU cluster) |

---

## 2. Chi Phí Triển Khai

### Hạ tầng GPU (nếu khách thuê cloud)
| GPU | Provider | $/giờ | $/tháng (24/7) | Phù hợp |
|-----|----------|-------|----------------|---------|
| RTX 4090 (24GB) | TensorDock | $0.35 | ~$252 | Gói Pro |
| A40 (48GB) | RunPod | $0.39 | ~$281 | Gói Pro+ |
| L40S (48GB) | RunPod | $0.49 | ~$353 | Enterprise |
| A100 (80GB) | RunPod | $0.79 | ~$569 | Enterprise+ |
| H100 (80GB) | RunPod | $2.49 | ~$1,793 | Heavy training |

### Hạ tầng on-premise (khách tự mua)
| Cấu hình | Giá ước tính | Phù hợp |
|-----------|-------------|---------|
| 1x RTX 4090 + Server | $5,000-8,000 | Gói Pro |
| 2x A40 + Server | $15,000-20,000 | Enterprise |
| GPU cluster (4x A100) | $80,000-120,000 | Enterprise+ |

---

## 3. Dịch Vụ Bổ Sung

| Dịch vụ | Giá |
|---------|-----|
| Fine-tune model trên data khách hàng | $3,000-10,000 / model |
| Custom OCR training (font/script riêng) | $5,000-15,000 |
| Tích hợp vào hệ thống có sẵn (API/SDK) | $2,000-5,000 |
| Training team vận hành (2-3 ngày) | $1,500-3,000 |
| Bảo trì mở rộng (sau khi hết gói) | $500-2,000/tháng |

---

## 4. So Sánh Với Đối Thủ

| Tiêu chí | budAI | Viettel AI | OpenAI Enterprise |
|----------|-------|------------|-------------------|
| On-premise | ✅ | ✅ | ❌ (cloud only) |
| Tiếng Việt | ✅ Tốt | ✅ Tốt | ⚠️ OK |
| ĐNÁ languages | ✅ 6 ngôn ngữ | ❌ Chủ yếu VN | ⚠️ Hạn chế |
| OCR | ✅ PaddleOCR-VL | ✅ Custom | ❌ Không có |
| TTS | ✅ MMS + XTTS | ⚠️ Hạn chế | ✅ Whisper |
| Cost optimizer | ✅ Multi-provider | ❌ | ❌ |
| Giá license | $5K-80K | Cao hơn | $60K+/năm |
| Data privacy | ✅ 100% offline | ✅ | ❌ Data đi Mỹ |

> **Lợi thế chính**: Data không rời khỏi hạ tầng khách hàng + hỗ trợ ngôn ngữ ĐNÁ + giá cạnh tranh

---

## 5. Timeline Triển Khai

| Giai đoạn | Thời gian | Nội dung |
|-----------|-----------|----------|
| 1. Demo & POC | 1-2 tuần | Setup API, test với data mẫu |
| 2. Pilot | 2-4 tuần | Triển khai trên infra khách, test real data |
| 3. Fine-tune | 2-4 tuần | Tối ưu model cho domain cụ thể |
| 4. Production | 1-2 tuần | Go-live, monitoring, SLA |
| **Tổng** | **6-12 tuần** | |

---

*budAI 🙏 — AI từ bi, giá nhân từ*
