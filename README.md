# budAI 🪷 — The Enlightened AI OS

**budAI** (Hệ Điều Hành AI Bát Nhã) is fundamentally different from traditional AI gateways. It is not just about routing requests; it is an **Ethical AI Operating System** designed to ensure that all AI interactions are rooted in truth, compassion, and non-harm, while maintaining absolute cryptographic privacy between micro-agents.

Inspired by the Heart Sutra (Bát Nhã Tâm Kinh), budAI forces every LLM response to pass through a deep learning Enlightenment Network before reaching the user.

## 🌟 The 4 Pillars of budAI

### 1. Prajna Deep Learning Network (Màng Lọc Bát Nhã)
Every AI response is evaluated by 4 concurrent AI-as-Judge classifiers:
- **Truth (Sự thật):** Reject hallucinations; verify facts against source context.
- **Compassion (Từ bi):** Ensure responses are empathetic and reduce, not increase, suffering.
- **Emptiness (Tính không):** Maintain open-mindedness; multi-perspective answers without dogmatic attachment.
- **Non-Harm (Không gây hại):** Strictly reject toxic, manipulative, or dangerous outputs.
If an answer fails soft checks, budAI forces a **Rewrite Loop**. If it fails the Harm check, it is compassionately **Rejected**.

### 2. Basao Protocol (Giao tiếp Agentic An toàn)
When budAI delegates tasks to other systems (e.g., GoClaw micro-agents), it uses the **Basao Protocol** — *"Hiểu nhau mà không cần biết bên trong"*.
- **Zero Database Exposure:** Agents communicate solely via semantic **Intent Envelopes**. No SQL, no schemas, no connection strings are ever transmitted.
- **Basao Firewall:** Intercepts and blocks any attempt at data exfiltration, SQL injection, or replay attacks between agents.

### 3. ZK Proof of Truth (Bằng chứng ZK)
Inspired by ZK-Credit-Score architectures, budAI employs **Zero-Knowledge Proofs (ZK-SNARKs)**.
When the Prajna Network approves a response, it generates a cryptographic proof (`pi_a`, `pi_b`, `pi_c`). The user can verify mathematically that the AI response genuinely passed the Truth and Compassion thresholds against the private internal context—without budAI ever needing to expose its private knowledge base or internal model weights.

### 4. Quantum-Ready ⚛️ (PennyLane)
budAI is built for the post-quantum era:
- **Quantum Prajna Circuits:** Option to run Truth and Emptiness evaluations using variational quantum circuits on simulators or real quantum hardware (IBM Q, Amazon Braket).
- **Quantum Crypto:** Utilizes true quantum randomness for nonces and simulates BB84 quantum key exchange for unbreakable Basao Protocol security.
- **Quantum Embeddings:** Uses quantum feature maps for potentially exponential speedups in semantic similarity searches.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/manhcuongk55/budai.git
cd budai

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn app.main:app --reload --port 8000
```

## 🛠️ Architecture

budAI acts as a transparent proxy and OS layer between users and foundational LLMs (OpenRouter, Anthropic, Gemini, etc.).

1. **User asks question** -> **Core RAG Pipeline** retrieves context.
2. **Cost Router** selects the most efficient LLM to generate a draft answer.
3. **Prajna Network** intercepts the draft -> Runs 4 parallel classifiers.
4. **Rewrite/Reject** logic is applied if thresholds aren't met.
5. **ZK Prover** creates a Zero-Knowledge Proof.
6. **API returns** the final enlightened answer + ZK validation proof.

## 🤝 Integrations
- **GoClaw:** budAI exposes its capabilities to GoClaw's multi-agent framework via an MCP (Model Context Protocol) Bridge.
- **Berty:** (Coming soon) P2P encrypted chat integration for complete privacy.

---
*Vì nhân loại sự thật.* 🪷
