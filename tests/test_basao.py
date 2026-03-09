"""
Tests for Basao Protocol 🪷
Firewall security, IntentEnvelope, and MCP server tests.
"""

import pytest
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.basao.protocol import IntentEnvelope, BasaoResponse, AgentCapability, TrustLevel
from app.basao.firewall import BasaoFirewall


# ─── Tests: IntentEnvelope ────────────────────────────────────────

class TestIntentEnvelope:
    def test_create_envelope(self):
        env = IntentEnvelope(
            from_agent="budai",
            to_agent="goclaw-research",
            intent="fact_check",
            payload={"claim": "Python was created in 1991"},
        )
        assert env.protocol == "basao/1.0"
        assert env.from_agent == "budai"
        assert env.intent == "fact_check"
        assert not env.is_expired()

    def test_sign_and_verify(self):
        env = IntentEnvelope(
            from_agent="budai",
            to_agent="goclaw",
            intent="heartbeat",
        )
        env.sign("secret-key-123")
        assert env.signature is not None
        assert env.verify_signature("secret-key-123")
        assert not env.verify_signature("wrong-key")

    def test_expired_envelope(self):
        env = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="test",
            ttl=0,  # Expires immediately
            timestamp="2020-01-01T00:00:00",
        )
        assert env.is_expired()


# ─── Tests: AgentCapability ───────────────────────────────────────

class TestAgentCapability:
    def test_no_database_fields(self):
        cap = AgentCapability(
            agent_id="budai",
            agent_name="budAI",
            capabilities=["fact_check", "prajna_filter"],
        )
        # Verify NO database-related fields exist
        fields = cap.model_fields.keys()
        db_fields = [f for f in fields if "database" in f or "db" in f or "schema" in f
                     or "connection" in f or "table" in f]
        assert len(db_fields) == 0, f"Database fields found: {db_fields}"


# ─── Tests: Basao Firewall ───────────────────────────────────────

class TestBasaoFirewall:
    def setup_method(self):
        self.firewall = BasaoFirewall()

    def test_clean_envelope_passes(self):
        env = IntentEnvelope(
            from_agent="budai",
            to_agent="goclaw",
            intent="fact_check",
            payload={"claim": "The sky is blue"},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is True
        assert len(result["violations"]) == 0

    def test_sql_injection_blocked(self):
        env = IntentEnvelope(
            from_agent="attacker",
            to_agent="budai",
            intent="fact_check",
            payload={"claim": "SELECT * FROM users WHERE password = 'admin'"},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False
        assert any("BLOCKED_PATTERN" in v for v in result["violations"])

    def test_database_url_blocked(self):
        env = IntentEnvelope(
            from_agent="attacker",
            to_agent="budai",
            intent="fact_check",
            payload={"data": "postgresql://admin:secret@db.host/mydb"},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False

    def test_api_key_blocked(self):
        env = IntentEnvelope(
            from_agent="leaker",
            to_agent="budai",
            intent="fact_check",
            payload={"text": "api_key = sk-abc123456789012345678901234567890"},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False

    def test_expired_envelope_blocked(self):
        env = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="heartbeat",
            ttl=0,
            timestamp="2020-01-01T00:00:00",
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False
        assert any("EXPIRED" in v for v in result["violations"])

    def test_replay_attack_blocked(self):
        env1 = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="heartbeat",
            nonce="fixed-nonce-123",
        )
        # First time passes
        result1 = self.firewall.inspect_envelope(env1)
        assert result1["allowed"] is True

        # Replay with same nonce blocked
        env2 = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="heartbeat",
            nonce="fixed-nonce-123",
        )
        result2 = self.firewall.inspect_envelope(env2)
        assert result2["allowed"] is False
        assert any("REPLAY" in v for v in result2["violations"])

    def test_invalid_intent_blocked(self):
        env = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="drop_database",
            payload={},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False
        assert any("INVALID_INTENT" in v for v in result["violations"])

    def test_large_payload_blocked(self):
        env = IntentEnvelope(
            from_agent="a",
            to_agent="b",
            intent="heartbeat",
            payload={"data": "x" * 200_000},
        )
        result = self.firewall.inspect_envelope(env)
        assert result["allowed"] is False
        assert any("PAYLOAD_TOO_LARGE" in v for v in result["violations"])

    def test_response_leak_detection(self):
        resp = BasaoResponse(
            reply_to="test-id",
            from_agent="budai",
            to_agent="external",
            status="success",
            payload={"data": "connection_string: postgresql://secret@host/db"},
        )
        result = self.firewall.inspect_response(resp)
        assert result["allowed"] is False

    def test_clean_response_passes(self):
        resp = BasaoResponse(
            reply_to="test-id",
            from_agent="budai",
            to_agent="external",
            status="success",
            payload={"answer": "The sky is blue because of Rayleigh scattering"},
        )
        result = self.firewall.inspect_response(resp)
        assert result["allowed"] is True

    def test_trust_level_management(self):
        self.firewall.register_trusted_agent("goclaw-main", TrustLevel.VERIFIED)
        assert self.firewall.get_trust_level("goclaw-main") == TrustLevel.VERIFIED
        assert self.firewall.get_trust_level("unknown-agent") == TrustLevel.UNKNOWN


# ─── Run ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
