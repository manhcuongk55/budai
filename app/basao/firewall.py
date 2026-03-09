"""
Basao Firewall — Ensures zero database exposure in inter-agent communication.
Blocks any attempt to leak database structure, queries, or connection info.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Set

from app.basao.protocol import IntentEnvelope, BasaoResponse, TrustLevel

logger = logging.getLogger("budai.basao.firewall")


# ─── Blocked Patterns ────────────────────────────────────────────────

# SQL patterns — block any database query language
SQL_PATTERNS = [
    r'\bSELECT\b', r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b',
    r'\bDROP\b', r'\bCREATE\s+TABLE\b', r'\bALTER\s+TABLE\b',
    r'\bJOIN\b', r'\bWHERE\b.*=', r'\bFROM\s+\w+\b',
]

# Database object patterns — block internal structure references
DB_OBJECT_PATTERNS = [
    r'\bdb\.', r'\bcollection\.', r'\bcursor\.',
    r'\bconnection_string\b', r'\bdatabase_url\b',
    r'\bDATABASE_URL\b', r'\bDB_HOST\b', r'\bDB_PASSWORD\b',
    r'\btable_name\b', r'\bschema\b', r'\bmigration\b',
    r'\bpgvector\b', r'\bchromadb\b', r'\bpostgresql://\b',
    r'\bmongodb://\b', r'\bredis://\b', r'\bmysql://\b',
]

# Credential patterns — block any credential leak
CREDENTIAL_PATTERNS = [
    r'(?:api[_-]?key|secret|password|token)\s*[=:]\s*\S+',
    r'sk-[a-zA-Z0-9]{20,}',  # OpenAI-style API keys
    r'Bearer\s+[a-zA-Z0-9\-._~+/]+=*',  # Bearer tokens
]

# Path traversal patterns
PATH_PATTERNS = [
    r'\.\./\.\./',
    r'[/\\]etc[/\\](passwd|shadow)',
    r'[/\\]\.env\b',
]


class BasaoFirewall:
    """
    Firewall for Basao Protocol — prevents database exposure and credential leaks.
    Every Intent Envelope must pass through this before processing.
    """

    def __init__(self):
        self._used_nonces: Set[str] = set()
        self._max_nonces = 10000
        self._trusted_agents: Dict[str, TrustLevel] = {}
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for performance."""
        all_patterns = SQL_PATTERNS + DB_OBJECT_PATTERNS + CREDENTIAL_PATTERNS + PATH_PATTERNS
        self._blocked_regex = [re.compile(p, re.IGNORECASE) for p in all_patterns]

    def inspect_envelope(self, envelope: IntentEnvelope) -> Dict[str, Any]:
        """
        Full security inspection of an Intent Envelope.
        Returns dict with 'allowed' bool and 'violations' list.
        """
        violations = []

        # 1. Check TTL
        if envelope.is_expired():
            violations.append("EXPIRED: Envelope TTL exceeded")

        # 2. Check replay attack (nonce reuse)
        if envelope.nonce in self._used_nonces:
            violations.append("REPLAY: Nonce already used")
        else:
            self._used_nonces.add(envelope.nonce)
            # Prevent memory leak
            if len(self._used_nonces) > self._max_nonces:
                # Remove oldest half
                to_remove = list(self._used_nonces)[:self._max_nonces // 2]
                for n in to_remove:
                    self._used_nonces.discard(n)

        # 3. Scan payload for blocked patterns
        payload_str = self._flatten_to_string(envelope.payload)
        for pattern in self._blocked_regex:
            match = pattern.search(payload_str)
            if match:
                violations.append(f"BLOCKED_PATTERN: '{match.group()}' detected in payload")

        # 4. Check intent is valid
        valid_intents = {
            "fact_check", "knowledge_query", "dharma_query",
            "prajna_filter", "truth_eval", "compassion_eval", "harm_detect",
            "route_to_cheapest", "route_to_best",
            "delegate", "handoff", "team_task", "heartbeat",
            "capability_query", "agent_discover",
        }
        if envelope.intent not in valid_intents:
            violations.append(f"INVALID_INTENT: '{envelope.intent}' is not a recognized intent")

        # 5. Check payload size (prevent data exfiltration)
        payload_size = len(payload_str)
        if payload_size > 100_000:  # 100KB max
            violations.append(f"PAYLOAD_TOO_LARGE: {payload_size} bytes (max 100KB)")

        allowed = len(violations) == 0

        if not allowed:
            logger.warning(
                f"🛡️ Basao Firewall BLOCKED envelope {envelope.envelope_id[:8]} "
                f"from {envelope.from_agent}: {violations}"
            )
        else:
            logger.info(
                f"🛡️ Basao Firewall PASSED envelope {envelope.envelope_id[:8]} "
                f"({envelope.from_agent} → {envelope.to_agent}: {envelope.intent})"
            )

        return {"allowed": allowed, "violations": violations}

    def inspect_response(self, response: BasaoResponse) -> Dict[str, Any]:
        """Inspect outgoing response for data leaks."""
        violations = []
        payload_str = self._flatten_to_string(response.payload)

        for pattern in self._blocked_regex:
            match = pattern.search(payload_str)
            if match:
                violations.append(f"OUTBOUND_LEAK: '{match.group()}' in response payload")

        allowed = len(violations) == 0
        if not allowed:
            logger.warning(f"🛡️ Basao Firewall BLOCKED outbound response: {violations}")

        return {"allowed": allowed, "violations": violations}

    def register_trusted_agent(self, agent_id: str, trust_level: TrustLevel):
        """Register an agent with a specific trust level."""
        self._trusted_agents[agent_id] = trust_level
        logger.info(f"🛡️ Agent '{agent_id}' registered as {trust_level.value}")

    def get_trust_level(self, agent_id: str) -> TrustLevel:
        """Get the trust level of an agent."""
        return self._trusted_agents.get(agent_id, TrustLevel.UNKNOWN)

    def _flatten_to_string(self, data: Any) -> str:
        """Recursively flatten a dict/list to a single string for scanning."""
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            return " ".join(self._flatten_to_string(v) for v in data.values())
        if isinstance(data, (list, tuple)):
            return " ".join(self._flatten_to_string(v) for v in data)
        return str(data)


# Singleton
basao_firewall = BasaoFirewall()
