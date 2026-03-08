"""Provider pricing registry — real-time cost data for AI APIs."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class TaskType(str, Enum):
    EMBEDDING = "embedding"
    GENERATION = "generation"


class Strategy(str, Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    BEST = "best"


@dataclass
class ModelPricing:
    """Pricing info for a specific model."""
    provider: str
    model: str
    task_type: TaskType
    input_cost_per_million: float  # $/1M tokens
    output_cost_per_million: float = 0.0  # $/1M tokens (embeddings = 0)
    quality_score: float = 0.5  # 0-1, subjective quality rating
    avg_latency_ms: int = 1000  # average response time
    max_tokens: int = 4096
    supports_vietnamese: bool = True
    notes: str = ""


# ═══════════════════════════════════════════════════════
#  PRICING REGISTRY — Updated March 2026
# ═══════════════════════════════════════════════════════

EMBEDDING_MODELS: List[ModelPricing] = [
    ModelPricing(
        provider="huggingface",
        model="sentence-transformers/all-MiniLM-L6-v2",
        task_type=TaskType.EMBEDDING,
        input_cost_per_million=0.0,
        quality_score=0.65,
        avg_latency_ms=500,
        max_tokens=512,
        notes="🆓 FREE — no API key needed!",
    ),
    ModelPricing(
        provider="openai",
        model="text-embedding-3-small",
        task_type=TaskType.EMBEDDING,
        input_cost_per_million=0.02,
        quality_score=0.75,
        avg_latency_ms=200,
        max_tokens=8191,
        notes="Best value for RAG",
    ),
    ModelPricing(
        provider="openai",
        model="text-embedding-3-large",
        task_type=TaskType.EMBEDDING,
        input_cost_per_million=0.13,
        quality_score=0.90,
        avg_latency_ms=300,
        max_tokens=8191,
        notes="Higher quality",
    ),
    ModelPricing(
        provider="google",
        model="text-embedding-004",
        task_type=TaskType.EMBEDDING,
        input_cost_per_million=0.006,
        quality_score=0.70,
        avg_latency_ms=250,
        max_tokens=2048,
        notes="Very cheap, decent quality",
    ),
]

GENERATION_MODELS: List[ModelPricing] = [
    ModelPricing(
        provider="huggingface",
        model="mistralai/Mistral-7B-Instruct-v0.3",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        quality_score=0.60,
        avg_latency_ms=3000,
        max_tokens=4096,
        notes="🆓 FREE — no API key needed!",
    ),
    ModelPricing(
        provider="openrouter",
        model="google/gemma-3-1b-it:free",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        quality_score=0.55,
        avg_latency_ms=2000,
        max_tokens=4096,
        notes="🆓 FREE via OpenRouter",
    ),
    ModelPricing(
        provider="deepseek",
        model="deepseek-chat",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.28,
        output_cost_per_million=0.42,
        quality_score=0.80,
        avg_latency_ms=2000,
        max_tokens=8192,
        notes="Cheapest quality option",
    ),
    ModelPricing(
        provider="google",
        model="gemini-2.5-flash",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.10,
        output_cost_per_million=0.40,
        quality_score=0.82,
        avg_latency_ms=1500,
        max_tokens=8192,
        notes="Very cheap + fast",
    ),
    ModelPricing(
        provider="openai",
        model="gpt-4o-mini",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.15,
        output_cost_per_million=0.60,
        quality_score=0.85,
        avg_latency_ms=1200,
        max_tokens=16384,
        notes="Reliable, good quality",
    ),
    ModelPricing(
        provider="groq",
        model="llama-3.3-70b-versatile",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.59,
        output_cost_per_million=0.79,
        quality_score=0.78,
        avg_latency_ms=500,
        max_tokens=8192,
        notes="Fastest inference",
    ),
    ModelPricing(
        provider="together",
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        task_type=TaskType.GENERATION,
        input_cost_per_million=0.88,
        output_cost_per_million=0.88,
        quality_score=0.78,
        avg_latency_ms=800,
        max_tokens=8192,
        notes="Open source, good for VN",
    ),
]

ALL_MODELS = EMBEDDING_MODELS + GENERATION_MODELS


def get_models_by_task(task_type: TaskType) -> List[ModelPricing]:
    """Get all models for a task type."""
    if task_type == TaskType.EMBEDDING:
        return EMBEDDING_MODELS
    return GENERATION_MODELS


def get_pricing_table() -> Dict:
    """Get full pricing table for API response."""
    return {
        "embedding": [
            {
                "provider": m.provider,
                "model": m.model,
                "input_cost_per_million": m.input_cost_per_million,
                "quality_score": m.quality_score,
                "notes": m.notes,
            }
            for m in EMBEDDING_MODELS
        ],
        "generation": [
            {
                "provider": m.provider,
                "model": m.model,
                "input_cost_per_million": m.input_cost_per_million,
                "output_cost_per_million": m.output_cost_per_million,
                "quality_score": m.quality_score,
                "notes": m.notes,
            }
            for m in GENERATION_MODELS
        ],
    }
