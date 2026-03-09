# Basao Protocol 🪷 — Inter-Agentic Communication Without Database Exposure

> *"Các AI giao tiếp như con người — hiểu ý nhau mà không cần biết bên trong."*

---

## Vấn đề

Khi nhiều micro-agentic AI hợp tác (budAI, GoClaw, partner systems):
- **Không được** lộ cấu trúc database nội bộ
- **Không được** truyền raw data giữa các hệ thống
- **Phải** giao tiếp qua ngữ nghĩa (semantic), không qua schema
- **Phải** chống hack, kể cả quantum computing trong tương lai

## Giải pháp: Basao Protocol

```
┌──────────────────────────────────────────────────────────┐
│                    Basao Protocol Layer                   │
│                                                          │
│  ┌──────────┐    Intent Envelope    ┌──────────────────┐ │
│  │  budAI   │ ◄══════════════════► │    GoClaw        │ │
│  │ (Python) │    (No DB exposed)    │    (Go)          │ │
│  └──────────┘                       └──────────────────┘ │
│       │              ▲                      │            │
│       │              │                      │            │
│  ┌──────────┐   ┌────────────┐   ┌──────────────────┐   │
│  │ Prajna   │   │  Basao     │   │  Partner         │   │
│  │ Filter   │   │  Firewall  │   │  Agent X         │   │
│  └──────────┘   └────────────┘   └──────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### 1. Intent Envelope (Phong bì Ý định)

Agents communicate qua **semantic intents**, không qua database queries:

```json
{
  "protocol": "basao/1.0",
  "envelope": {
    "from": "budai-prajna",
    "to": "goclaw-research-bot",
    "intent": "fact_check",
    "payload": {
      "claim": "Python was created in 1991",
      "confidence_required": 0.8
    },
    "signature": "ed25519:...",
    "nonce": "quantum-safe-nonce",
    "ttl": 30
  }
}
```

**Không có SQL, không có schema, không có database path** — chỉ có ý định và dữ liệu ngữ nghĩa.

### 2. Capability-Based Trust (Tin tưởng theo năng lực)

Mỗi agent khai báo **capabilities** (khả năng), không khai báo database:

```json
{
  "agent": "budai-prajna",
  "capabilities": ["fact_check", "compassion_eval", "harm_detect", "dharma_rag"],
  "trust_level": "verified",
  "prajna_compliant": true
}
```

Agent A không cần biết Agent B dùng PostgreSQL hay ChromaDB — chỉ cần biết B **có khả năng** `fact_check`.

### 3. Zero-Knowledge Proof Handshake

```
Agent A                    Basao Firewall                Agent B
   │                            │                           │
   │─── "I need fact_check" ───►│                           │
   │                            │── verify capability ─────►│
   │                            │◄── proof without DB ──────│
   │◄── "B can do it, safe" ────│                           │
   │══════ Intent Envelope ═════╪══════════════════════════►│
   │◄═════ Response ════════════╪═══════════════════════════│
```

### 4. Quantum-Safe Signatures

Mỗi envelope được ký bằng **post-quantum cryptography**:

| Layer | Algorithm | Purpose |
|-------|-----------|---------|
| Signing | CRYSTALS-Dilithium | Quantum-resistant digital signature |
| Encryption | CRYSTALS-Kyber | Key encapsulation (envelope encryption) |
| Hashing | SHA-3 | Integrity verification |
| Current fallback | Ed25519 + AES-256-GCM | Pre-quantum security |

---

## Integration: budAI ↔ GoClaw

### Mapping Architecture

| budAI Component | GoClaw Component | Basao Bridge |
|----------------|------------------|-------------|
| Prajna Filter (Python) | Quality Gates (Go) | Prajna → Quality Gate agent |
| CostRouter | Agent Delegation | Intent: `route_to_cheapest` |
| RAG Pipeline | Skill Search | Intent: `knowledge_query` |
| Self-Audit | Evaluate Loop | Generator-Evaluator with Prajna |

### Integration Method: MCP Bridge

GoClaw supports **MCP (Model Context Protocol)** — we create budAI as an MCP server that GoClaw agents can call:

```
GoClaw Agent
     │
     ▼
MCP Client (Go)
     │
     ▼ (stdio / HTTP)
┌─────────────────────┐
│ budAI MCP Server    │
│  - prajna_filter     │  ← tool
│  - dharma_query      │  ← tool
│  - cost_route        │  ← tool
│  - fact_check        │  ← tool
└─────────────────────┘
```

---

## Implementation Plan

### Phase 1: MCP Bridge (budAI ↔ GoClaw)

| File | Description |
|------|-------------|
| `app/basao/__init__.py` | Basao Protocol module |
| `app/basao/protocol.py` | Intent Envelope schema, signing, verification |
| `app/basao/firewall.py` | Capability-based access control |
| `app/basao/mcp_server.py` | budAI as MCP server for GoClaw |
| `app/basao/bridge.py` | GoClaw HTTP API client (agent delegation) |

### Phase 2: GoClaw Clone + Prajna Quality Gate

```bash
# Clone goclaw alongside budai
git clone https://github.com/nextlevelbuilder/goclaw.git
# Configure goclaw to use budAI Prajna as quality gate
```

### Phase 3: Quantum-Safe Crypto

Post-quantum signature library integration.

---

## Basao Firewall Rules

```python
# No database exposure — ever
FIREWALL_RULES = {
    "block_patterns": [
        "SELECT", "INSERT", "UPDATE", "DELETE",  # SQL
        "db.", "collection.", "cursor.",          # DB objects
        "connection_string", "database_url",     # Connection info
        "schema", "migration", "table_name",     # Structure info
    ],
    "allow_only": [
        "intent", "capability", "payload",       # Semantic only
        "claim", "question", "answer",           # Content only
        "score", "feedback", "action",           # Evaluation only
    ]
}
```

---

*Basao Protocol 🪷 — "Hiểu nhau mà không cần biết bên trong"*
