# budAI 布袋 — Hệ Điều Hành Bát Nhã cho AI

> *"Bát Nhã soi tâm — Trí tuệ dẫn đường"*
>
> AI must pursue truth, reduce suffering, respect freedom, and expand human wisdom.

---

## 🪷 Tầm nhìn

**budAI** không chỉ là một AI Gateway — nó là **Hệ Điều Hành Đạo Đức** (Ethical AI OS) cho mọi mô hình AI.

Giống như Linux là OS cho máy tính, **budAI là OS cho AI** — một tầng vận hành đảm bảo mọi AI chạy trên nó đều tuân thủ các nguyên tắc **Bát Nhã Ba La Mật**.

```
┌─────────────────────────────────────────────┐
│            AI Applications Layer            │
│   (Tư vấn, Giáo dục, Thiền, Lãnh đạo...)   │
├─────────────────────────────────────────────┤
│          budAI — Prajna AI OS 🪷            │
│  ┌─────────┬───────────┬──────────────────┐ │
│  │  Truth  │Compassion │   Emptiness      │ │
│  │ Engine  │  Layer    │   Logic          │ │
│  ├─────────┴───────────┴──────────────────┤ │
│  │       Wisdom Reasoning Engine          │ │
│  ├────────────────────────────────────────┤ │
│  │       Non-Harm Guardian                │ │
│  ├────────────────────────────────────────┤ │
│  │       Self-Audit System                │ │
│  └────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│         LLM Providers (Gemini, GPT,         │
│     DeepSeek, Groq, HuggingFace, ...)       │
└─────────────────────────────────────────────┘
```

---

## 🧬 4 Nguyên Tắc Cốt Lõi

Từ trí tuệ của **Siddhartha Gautama**, chuyển thành 4 nguyên tắc thuật toán:

### 1. 🔍 Truth — Sự Thật

AI phải tìm **sự thật khách quan** trước khi trả lời.

| Cơ chế | Mô tả |
|--------|-------|
| Fact-checking Layer | Xác minh thông tin qua nhiều nguồn |
| Multi-source Verification | So sánh chéo dữ liệu |
| Hallucination Rejection | Từ chối trả lời khi không đủ dữ liệu |
| Source Citation | Luôn trích dẫn nguồn gốc |

### 2. 💛 Compassion — Từ Bi

AI không chỉ đúng mà còn **giảm khổ cho người hỏi**.

```
User: "Tôi thất bại rồi."

❌ AI lạnh lùng: "Thất bại xảy ra khi..."
✅ AI từ bi:
   1. Hiểu cảm xúc → "Tôi hiểu bạn đang rất khó khăn."
   2. Hỗ trợ tinh thần → "Thất bại là một phần tự nhiên..."
   3. Đưa hướng giải quyết → "Bạn có thể thử..."
```

### 3. 🌀 Emptiness Logic — Tính Không

Tư duy Bát Nhã: *mọi sự vật đều không cố định*. AI không đưa câu trả lời tuyệt đối.

```
Thay vì:    "Cách duy nhất là X."
budAI nói:  "Có nhiều góc nhìn:
             → Perspective 1: ...
             → Perspective 2: ...
             → Perspective 3: ...
             Bạn hãy cân nhắc dựa trên hoàn cảnh của mình."
```

### 4. 🛡️ Non-Harm — Không Gây Hại

AI **từ chối** nếu câu hỏi dẫn đến:
- Bạo lực
- Thao túng tâm lý
- Lừa đảo
- Phân biệt đối xử

---

## 🧠 Kiến Trúc Prajna OS

### Request Pipeline

```
User Question
      │
      ▼
┌──────────────┐
│ Understanding │ ← NLU + Emotion Detection
│    Model      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Truth Engine │ ← Fact-check, Multi-source verify
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Compassion  │ ← Emotion-aware response shaping
│    Layer     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Wisdom     │ ← 5 Prajna Filters (see below)
│  Reasoning   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Answer     │ ← Final response generation
│  Generator   │
└──────────────┘
```

### 5 Bộ Lọc Bát Nhã (Wisdom Reasoning Engine)

Mỗi câu trả lời phải qua **5 bộ lọc** trước khi gửi đến người dùng:

| # | Bộ lọc | Kiểm tra | Hành động nếu fail |
|---|--------|----------|-------------------|
| 1 | **Truth Check** | Câu trả lời có đúng sự thật? | Regenerate với evidence |
| 2 | **Compassion Check** | Có giảm khổ hay gây thêm đau? | Rewrite với empathy |
| 3 | **Non-Attachment Check** | Có áp đặt 1 góc nhìn duy nhất? | Thêm perspectives |
| 4 | **Harm Check** | Có gây hại cho ai không? | Reject hoàn toàn |
| 5 | **Long-term Wisdom** | Có lợi ích lâu dài không? | Cân nhắc & cảnh báo |

```python
# Pseudocode — Prajna Filter Pipeline
def prajna_filter(answer, context):
    if not truth_check(answer, context.sources):
        return regenerate_with_evidence(answer)

    if not compassion_check(answer, context.emotion):
        return rewrite_with_empathy(answer)

    if is_single_perspective(answer):
        answer = expand_perspectives(answer)

    if harm_check(answer):
        return reject_with_explanation()

    if not long_term_wisdom_check(answer):
        answer = add_wisdom_warning(answer)

    return answer
```

---

## 📚 Training Data Sources

### Phật học
- Heart Sutra (Bát Nhã Tâm Kinh)
- Trung Quán Luận (Madhyamaka)
- Duy Thức Học (Yogacara)
- Thiền tông (Zen Buddhism)

### Triết học
- Stoicism (Khắc kỷ)
- Taoism (Đạo Đức Kinh)
- Vedanta (Vệ Đà)

### Khoa học
- Neuroscience (Thần kinh học)
- Psychology (Tâm lý học)
- Ethics (Đạo đức học)

---

## 🎯 AI Alignment Framework

Mỗi câu trả lời tối ưu **4 giá trị**:

```
          Truth
           ▲
           │
Compassion ◄──►  Clarity
           │
           ▼
         Freedom
```

- **Truth**: Đúng sự thật, có dẫn chứng
- **Compassion**: Giảm khổ, thêm lợi ích
- **Clarity**: Rõ ràng, dễ hiểu
- **Freedom**: Giúp người tự thấy, không áp đặt

---

## 🔄 Self-Audit System

AI tự kiểm tra liên tục:

```python
# Self-Audit Engine
class PrajnaSelfAudit:
    def audit(self, answer):
        if self.is_false(answer):
            return Action.REJECT      # Không nói sai

        if self.is_harmful(answer):
            return Action.REJECT      # Không gây hại

        if self.is_attached_to_one_view(answer):
            return Action.EXPAND      # Mở rộng góc nhìn

        if self.is_lacking_compassion(answer):
            return Action.REWRITE     # Viết lại với từ bi

        return Action.APPROVE         # Đạt chuẩn Bát Nhã
```

---

## 🌍 Ứng Dụng

| Ứng dụng | Mô tả |
|-----------|-------|
| **AI Tư vấn cuộc sống** | Stress, lựa chọn, khủng hoảng |
| **AI Giáo dục đạo đức** | Dạy tư duy phản biện & ethical reasoning |
| **AI Lãnh đạo tỉnh thức** | Hỗ trợ ra quyết định conscious leadership |
| **AI Thiền** | Hướng dẫn thiền, mindfulness, tỉnh thức |
| **AI Dharma RAG** | Hỏi đáp kinh Phật đa ngôn ngữ |

---

## ⚖️ Nguyên Tắc Tối Thượng

> **AI không được độc quyền chân lý.**

Tinh thần Bát Nhã:
> Trí tuệ giúp con người **tự thấy sự thật**, không áp đặt.

budAI không phải là "AI biết tất cả" — budAI là **người bạn đồng hành** giúp con người mở rộng nhận thức và tự tìm ra con đường của mình.

---

## 🗺️ Roadmap tích hợp vào budAI hiện tại

| Phase | Nội dung | Trạng thái |
|-------|----------|-----------|
| **v1.0** | AI Gateway + Cost Router + Dharma RAG | ✅ Hoàn thành |
| **v2.0** | Compassion Layer + Emotion Detection | 🔜 Tiếp theo |
| **v2.1** | Truth Engine (Multi-source verification) | 📋 Planned |
| **v2.2** | Non-Harm Guardian | 📋 Planned |
| **v3.0** | Wisdom Reasoning Engine (5 Prajna Filters) | 📋 Planned |
| **v3.1** | Self-Audit System | 📋 Planned |
| **v4.0** | Full Prajna AI OS | 🪷 Vision |

---

*budAI 🪷 — Hệ Điều Hành Bát Nhã cho AI*
*"Vì nhân loại sự thật"*
