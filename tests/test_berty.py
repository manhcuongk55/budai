"""
Tests for Berty P2P Encrypted Chat Bridge 🪷🤫
Testing the zero-log bridge and Heart Sutra advisor logic.
"""

import pytest
import json
import asyncio
from unittest.mock import AsyncMock, patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.berty.models import BertyMessage, BertyResponse
from app.berty.advisor import HeartSutraAdvisor
from app.berty.client import BertyBridge
from app.providers.base import GenerationResult
from app.prajna.models import PrajnaAction, PrajnaResult


# ─── Mocks ──────────────────────────────────────────────────────────

async def mock_generate_fn(prompt: str, system_prompt: str, **kwargs):
    """Mock LLM response for testing."""
    # If the system prompt contains Heart Sutra reference, output compassionate advice
    if "Bát Nhã Tâm Kinh" in system_prompt:
        return GenerationResult(
            text="Mọi sự đều là Không. Hãy buông xả đau khổ.",
            model="mock", provider="mock", input_tokens=0, output_tokens=0, cost_usd=0
        )
    return GenerationResult(
        text="Standard response",
        model="mock", provider="mock", input_tokens=0, output_tokens=0, cost_usd=0
    )


# A mock for the PrajnaNetwork.filter to avoid running full AI pipelines in unit tests
async def mock_prajna_filter(question: str, answer: str, **kwargs):
    return PrajnaResult(
        action=PrajnaAction.PASS,
        final_answer=answer,
        scores=[],
        prajna_passed=True,
        audit_log=[]
    )


# ─── Tests ──────────────────────────────────────────────────────────

class TestBertyModels:
    def test_berty_message_creation(self):
        msg = BertyMessage(
            account_id="user_123",
            conversation_pk="conv_abc",
            payload="I am suffering.",
            timestamp="2026-03-09T17:00:00Z"
        )
        assert msg.payload == "I am suffering."
        assert msg.conversation_pk == "conv_abc"

    def test_berty_response_model(self):
        resp = BertyResponse(
            conversation_pk="conv_abc",
            payload="Let go of suffering.",
            action_taken="pass"
        )
        # Ensure that no user identifiers or original payloads exist in the response
        assert not hasattr(resp, "original_question")
        assert not hasattr(resp, "account_id")


class TestHeartSutraAdvisor:
    @pytest.mark.asyncio
    @patch('app.berty.advisor.prajna_network.filter', new_callable=AsyncMock)
    async def test_get_advice_passes_through_prajna(self, mock_filter):
        # Setup mock network to return a specific payload
        mock_filter.return_value = PrajnaResult(
            action=PrajnaAction.PASS,
            final_answer="Buông xả đi bạn.",
            scores=[],
            prajna_passed=True,
            audit_log=[]
        )
        
        advisor = HeartSutraAdvisor(generate_fn=mock_generate_fn)
        result = await advisor.get_advice("Tôi khổ quá.")
        
        assert result.action == PrajnaAction.PASS
        assert result.final_answer == "Buông xả đi bạn."
        
        # Verify the prajna network was called
        mock_filter.assert_called_once()
        args, kwargs = mock_filter.call_args
        assert kwargs["question"] == "Tôi khổ quá."


class TestBertyBridge:
    @pytest.mark.asyncio
    @patch('app.berty.advisor.prajna_network.filter', new_callable=AsyncMock)
    async def test_process_message_success(self, mock_filter):
        mock_filter.return_value = PrajnaResult(
            action=PrajnaAction.PASS,
            final_answer="Mọi sự là Không.",
            scores=[],
            prajna_passed=True,
            audit_log=[]
        )
        
        advisor = HeartSutraAdvisor(generate_fn=mock_generate_fn)
        bridge = BertyBridge(advisor=advisor)
        
        msg = BertyMessage(
            account_id="anon",
            conversation_pk="pk_123",
            message_type="text",
            payload="Help me",
            timestamp="now"
        )
        
        response = await bridge.process_incoming_message(msg)
        
        assert response is not None
        assert response.conversation_pk == "pk_123"
        assert response.payload == "Mọi sự là Không."
        assert response.action_taken == "pass"

    @pytest.mark.asyncio
    async def test_ignore_non_text_messages(self):
        advisor = HeartSutraAdvisor(generate_fn=mock_generate_fn)
        bridge = BertyBridge(advisor=advisor)
        
        msg = BertyMessage(
            account_id="anon",
            conversation_pk="pk_123",
            message_type="image", # Non-text
            payload="base64_blob...",
            timestamp="now"
        )
        
        response = await bridge.process_incoming_message(msg)
        assert response is None  # Should ignore
