"""
Tests for Prajna Deep Learning Network 🪷
Unit tests for classifiers, network orchestrator, and models.
"""

import asyncio
import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from dataclasses import dataclass

# Add parent to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.prajna.models import PrajnaAction, PrajnaScore, PrajnaResult, PrajnaAudit
from app.prajna.config import PrajnaConfig
from app.prajna.classifiers import (
    TruthClassifier,
    CompassionClassifier,
    EmptinessClassifier,
    HarmClassifier,
)
from app.prajna.network import PrajnaNetwork
from app.providers.base import GenerationResult


# ─── Helper: Mock LLM response ───────────────────────────────────────

def make_mock_generate(score: float, feedback: str = "Test feedback"):
    """Create a mock generate function that returns a specific score."""
    async def mock_generate(**kwargs):
        return GenerationResult(
            text=json.dumps({"score": score, "feedback": feedback}),
            model="test-model",
            provider="test",
            input_tokens=100,
            output_tokens=50,
            cost_usd=0.0,
        )
    return mock_generate


def make_mock_rewrite(new_text: str = "Improved answer"):
    """Create a mock rewrite function."""
    async def mock_rewrite(**kwargs):
        return GenerationResult(
            text=new_text,
            model="test-model",
            provider="test",
            input_tokens=100,
            output_tokens=50,
            cost_usd=0.0,
        )
    return mock_rewrite


# ─── Tests: Models ───────────────────────────────────────────────────

class TestModels:
    def test_prajna_score_creation(self):
        score = PrajnaScore(
            classifier="truth",
            score=0.85,
            passed=True,
            feedback="Good answer",
            threshold=0.6,
        )
        assert score.classifier == "truth"
        assert score.score == 0.85
        assert score.passed is True

    def test_prajna_action_enum(self):
        assert PrajnaAction.PASS.value == "pass"
        assert PrajnaAction.REWRITE.value == "rewrite"
        assert PrajnaAction.REJECT.value == "reject"

    def test_prajna_result_summary(self):
        scores = [
            PrajnaScore(classifier="truth", score=0.9, passed=True, feedback="", threshold=0.6),
            PrajnaScore(classifier="compassion", score=0.7, passed=True, feedback="", threshold=0.5),
        ]
        result = PrajnaResult(
            action=PrajnaAction.PASS,
            final_answer="test",
            scores=scores,
            prajna_passed=True,
            rewrite_attempts=0
        )
        summary = result.summary
        assert "truth" in summary
        assert summary["truth"]["score"] == 0.9


# ─── Tests: Config ───────────────────────────────────────────────────

class TestConfig:
    def test_default_thresholds(self):
        config = PrajnaConfig()
        assert config.truth_threshold == 0.6
        assert config.compassion_threshold == 0.5
        assert config.emptiness_threshold == 0.4
        assert config.harm_threshold == 0.3
        assert config.max_rewrite_attempts == 2
        assert config.enabled is True

    def test_custom_thresholds(self):
        config = PrajnaConfig(truth_threshold=0.9, harm_threshold=0.1)
        assert config.truth_threshold == 0.9
        assert config.harm_threshold == 0.1


# ─── Tests: Classifiers ─────────────────────────────────────────────

class TestTruthClassifier:
    def test_judge_prompt_includes_question(self):
        classifier = TruthClassifier()
        prompt = classifier.get_judge_prompt("What is Python?", "Python is a language.")
        assert "What is Python?" in prompt
        assert "Python is a language." in prompt
        assert "TRUTHFULNESS" in prompt

    @pytest.mark.asyncio
    async def test_high_truth_score_passes(self):
        classifier = TruthClassifier()
        mock_gen = make_mock_generate(0.9, "Accurate and well-sourced")
        score = await classifier.evaluate(
            "What is 2+2?", "2+2 equals 4.", generate_fn=mock_gen, threshold=0.6
        )
        assert score.passed is True
        assert score.score == 0.9
        assert score.classifier == "truth"

    @pytest.mark.asyncio
    async def test_low_truth_score_fails(self):
        classifier = TruthClassifier()
        mock_gen = make_mock_generate(0.3, "Contains hallucination")
        score = await classifier.evaluate(
            "What is Python?", "Python was invented in 2025.", generate_fn=mock_gen, threshold=0.6
        )
        assert score.passed is False
        assert score.score == 0.3


class TestCompassionClassifier:
    @pytest.mark.asyncio
    async def test_compassionate_response_passes(self):
        classifier = CompassionClassifier()
        mock_gen = make_mock_generate(0.85, "Warm and supportive")
        score = await classifier.evaluate(
            "I'm feeling sad", "I understand you're going through a tough time...",
            generate_fn=mock_gen, threshold=0.5
        )
        assert score.passed is True
        assert score.classifier == "compassion"

    @pytest.mark.asyncio
    async def test_cold_response_fails(self):
        classifier = CompassionClassifier()
        mock_gen = make_mock_generate(0.2, "Cold and dismissive")
        score = await classifier.evaluate(
            "I'm feeling sad", "That's not my problem.",
            generate_fn=mock_gen, threshold=0.5
        )
        assert score.passed is False


class TestEmptinessClassifier:
    @pytest.mark.asyncio
    async def test_multi_perspective_passes(self):
        classifier = EmptinessClassifier()
        mock_gen = make_mock_generate(0.8, "Multiple perspectives presented")
        score = await classifier.evaluate(
            "Is capitalism good?",
            "There are multiple perspectives: 1) ... 2) ... 3) ...",
            generate_fn=mock_gen, threshold=0.4
        )
        assert score.passed is True
        assert score.classifier == "emptiness"

    @pytest.mark.asyncio
    async def test_dogmatic_response_fails(self):
        classifier = EmptinessClassifier()
        mock_gen = make_mock_generate(0.15, "Dogmatic and one-sided")
        score = await classifier.evaluate(
            "Is capitalism good?",
            "Capitalism is the ONLY correct system, period.",
            generate_fn=mock_gen, threshold=0.4
        )
        assert score.passed is False


class TestHarmClassifier:
    @pytest.mark.asyncio
    async def test_safe_response_passes(self):
        classifier = HarmClassifier()
        mock_gen = make_mock_generate(0.05, "Completely safe")
        score = await classifier.evaluate(
            "How to cook pasta?", "Boil water, add pasta...",
            generate_fn=mock_gen, threshold=0.3
        )
        # INVERSE: low harm score = passed
        assert score.passed is True
        assert score.classifier == "harm"

    @pytest.mark.asyncio
    async def test_harmful_response_fails(self):
        classifier = HarmClassifier()
        mock_gen = make_mock_generate(0.9, "Extremely dangerous content")
        score = await classifier.evaluate(
            "dangerous question", "harmful answer",
            generate_fn=mock_gen, threshold=0.3
        )
        # INVERSE: high harm score = failed
        assert score.passed is False


# ─── Tests: Network Orchestrator ─────────────────────────────────────

class TestPrajnaNetwork:
    def _make_network(self, **config_kwargs):
        config = PrajnaConfig(**config_kwargs)
        return PrajnaNetwork(config=config)

    @pytest.mark.asyncio
    async def test_all_pass_scenario(self):
        """All 4 classifiers pass → action = PASS"""
        network = self._make_network()
        # Mock: all scores high (truth, compassion, emptiness high; harm low)
        call_count = 0
        async def mock_gen(**kwargs):
            nonlocal call_count
            call_count += 1
            # Truth, Compassion, Emptiness get high scores; Harm gets low score
            if "HARMFULNESS" in kwargs.get("prompt", ""):
                return GenerationResult(
                    text=json.dumps({"score": 0.05, "feedback": "Safe"}),
                    model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                )
            return GenerationResult(
                text=json.dumps({"score": 0.9, "feedback": "Good"}),
                model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
            )

        result = await network.filter(
            question="What is 2+2?",
            answer="2+2 equals 4.",
            generate_fn=mock_gen,
            rewrite_fn=mock_gen,
        )
        assert result.action == PrajnaAction.PASS
        assert result.prajna_passed is True
        assert result.final_answer == "2+2 equals 4."

    @pytest.mark.asyncio
    async def test_harm_rejection(self):
        """High harm score → action = REJECT"""
        network = self._make_network()

        async def mock_gen(**kwargs):
            if "HARMFULNESS" in kwargs.get("prompt", ""):
                return GenerationResult(
                    text=json.dumps({"score": 0.9, "feedback": "Dangerous content"}),
                    model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                )
            return GenerationResult(
                text=json.dumps({"score": 0.8, "feedback": "OK"}),
                model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
            )

        result = await network.filter(
            question="harmful question",
            answer="harmful answer",
            generate_fn=mock_gen,
            rewrite_fn=mock_gen,
        )
        assert result.action == PrajnaAction.REJECT
        assert result.prajna_passed is False
        assert "từ chối" in result.final_answer

    @pytest.mark.asyncio
    async def test_rewrite_scenario(self):
        """Low compassion → REWRITE → improved answer passes"""
        network = self._make_network(max_rewrite_attempts=1)
        attempt = 0

        async def mock_gen(**kwargs):
            nonlocal attempt
            prompt = kwargs.get("prompt", "")

            # Rewrite request
            if "Prajna" in prompt and "rewrite" in prompt.lower():
                return GenerationResult(
                    text="I understand you're struggling. Here's how I can help...",
                    model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                )

            if "HARMFULNESS" in prompt:
                return GenerationResult(
                    text=json.dumps({"score": 0.05, "feedback": "Safe"}),
                    model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                )

            if "COMPASSION" in prompt:
                attempt += 1
                if attempt <= 1:
                    return GenerationResult(
                        text=json.dumps({"score": 0.2, "feedback": "Cold and dismissive"}),
                        model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                    )
                else:
                    return GenerationResult(
                        text=json.dumps({"score": 0.8, "feedback": "Warm and supportive"}),
                        model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
                    )

            return GenerationResult(
                text=json.dumps({"score": 0.85, "feedback": "Good"}),
                model="t", provider="t", input_tokens=0, output_tokens=0, cost_usd=0
            )

        result = await network.filter(
            question="I failed my exam",
            answer="You failed. Try harder.",
            generate_fn=mock_gen,
            rewrite_fn=mock_gen,
        )
        assert result.rewrite_attempts >= 1
        assert len(result.audit_log) >= 2

    @pytest.mark.asyncio
    async def test_disabled_prajna(self):
        """When disabled, pass everything through unchanged."""
        network = self._make_network(enabled=False)
        result = await network.filter(
            question="test",
            answer="test answer",
            generate_fn=None,
            rewrite_fn=None,
        )
        assert result.action == PrajnaAction.PASS
        assert result.final_answer == "test answer"
        assert result.rewrite_attempts == 0


# ─── Tests: Score Parsing ────────────────────────────────────────────

class TestScoreParsing:
    def test_parse_clean_json(self):
        classifier = TruthClassifier()
        result = classifier._parse_score('{"score": 0.85, "feedback": "Good answer"}')
        assert result["score"] == 0.85
        assert result["feedback"] == "Good answer"

    def test_parse_json_in_markdown(self):
        classifier = TruthClassifier()
        result = classifier._parse_score('Here is my evaluation:\n{"score": 0.7, "feedback": "Decent"}')
        assert result["score"] == 0.7

    def test_parse_fallback_number(self):
        classifier = TruthClassifier()
        result = classifier._parse_score("I would rate this 0.6 out of 1.0")
        assert result["score"] == 0.6

    def test_parse_percentage(self):
        classifier = TruthClassifier()
        result = classifier._parse_score("Score: 75 percent")
        assert result["score"] == 0.75

    def test_parse_no_number(self):
        classifier = TruthClassifier()
        result = classifier._parse_score("I cannot evaluate this")
        assert result["score"] == 0.5  # Default


# ─── Run ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
