"""
Basao Protocol — Intent Envelope & Message Schema.
Communication via semantic intents, zero database exposure.
"""

import hashlib
import hmac
import json
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ─── Intent Types ─────────────────────────────────────────────────────

class IntentType(str, Enum):
    """Standard intent types for inter-agent communication."""
    # Knowledge
    FACT_CHECK = "fact_check"
    KNOWLEDGE_QUERY = "knowledge_query"
    DHARMA_QUERY = "dharma_query"

    # Evaluation (Prajna)
    PRAJNA_FILTER = "prajna_filter"
    TRUTH_EVAL = "truth_eval"
    COMPASSION_EVAL = "compassion_eval"
    HARM_DETECT = "harm_detect"

    # Routing
    ROUTE_TO_CHEAPEST = "route_to_cheapest"
    ROUTE_TO_BEST = "route_to_best"

    # Agent coordination
    DELEGATE = "delegate"
    HANDOFF = "handoff"
    TEAM_TASK = "team_task"
    HEARTBEAT = "heartbeat"

    # Discovery
    CAPABILITY_QUERY = "capability_query"
    AGENT_DISCOVER = "agent_discover"


class TrustLevel(str, Enum):
    """Trust levels for agent verification."""
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    VERIFIED = "verified"
    TRUSTED = "trusted"
    PRAJNA_CERTIFIED = "prajna_certified"  # Passed all 4 Prajna checks


# ─── Agent Capability ────────────────────────────────────────────────

class AgentCapability(BaseModel):
    """What an agent can do — NO database info exposed."""
    agent_id: str = Field(description="Unique agent identifier")
    agent_name: str = Field(description="Human-readable agent name")
    capabilities: List[str] = Field(description="List of intent types this agent handles")
    trust_level: TrustLevel = Field(default=TrustLevel.UNKNOWN)
    prajna_compliant: bool = Field(default=False, description="Whether agent passes Prajna filters")
    version: str = Field(default="1.0")

    # NO database fields — ever
    # NO schema fields — ever
    # NO connection strings — ever


# ─── Intent Envelope ──────────────────────────────────────────────────

class IntentEnvelope(BaseModel):
    """
    The core communication unit of Basao Protocol.
    Contains ONLY semantic data — zero database exposure.
    """
    # Protocol header
    protocol: str = Field(default="basao/1.0", description="Protocol version")
    envelope_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message ID")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Routing
    from_agent: str = Field(description="Sender agent ID")
    to_agent: str = Field(description="Target agent ID")
    intent: str = Field(description="Intent type (what you want)")
    reply_to: Optional[str] = Field(default=None, description="Envelope ID this is replying to")

    # Payload — semantic data only
    payload: Dict[str, Any] = Field(default_factory=dict, description="Intent-specific data")

    # Security
    signature: Optional[str] = Field(default=None, description="Digital signature (Ed25519/Dilithium)")
    nonce: str = Field(default_factory=lambda: uuid.uuid4().hex[:16], description="Anti-replay nonce")
    ttl: int = Field(default=30, description="Time-to-live in seconds")

    # Metadata
    priority: int = Field(default=5, ge=1, le=10, description="1=lowest, 10=highest")
    trace_id: Optional[str] = Field(default=None, description="Distributed tracing ID")

    def is_expired(self) -> bool:
        """Check if envelope has expired."""
        created = datetime.fromisoformat(self.timestamp)
        age = (datetime.utcnow() - created).total_seconds()
        return age > self.ttl

    def sign(self, secret_key: str) -> "IntentEnvelope":
        """Sign the envelope with HMAC-SHA256 (pre-quantum fallback)."""
        message = f"{self.envelope_id}:{self.from_agent}:{self.to_agent}:{self.intent}:{self.nonce}"
        self.signature = hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return self

    def verify_signature(self, secret_key: str) -> bool:
        """Verify the envelope signature."""
        if not self.signature:
            return False
        message = f"{self.envelope_id}:{self.from_agent}:{self.to_agent}:{self.intent}:{self.nonce}"
        expected = hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected)


# ─── Basao Response ──────────────────────────────────────────────────

class BasaoResponse(BaseModel):
    """Response to an Intent Envelope."""
    protocol: str = Field(default="basao/1.0")
    envelope_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    reply_to: str = Field(description="Original envelope ID")
    from_agent: str
    to_agent: str
    status: str = Field(description="success / error / rejected")
    payload: Dict[str, Any] = Field(default_factory=dict)
    signature: Optional[str] = None
    prajna_audit: Optional[Dict[str, Any]] = Field(default=None,
        description="Prajna filter results if applicable")


# ─── Basao Message Bus ───────────────────────────────────────────────

class BasaoMessage(BaseModel):
    """Internal message wrapper for the message bus."""
    envelope: IntentEnvelope
    received_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    processed: bool = False
    response: Optional[BasaoResponse] = None
