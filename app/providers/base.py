"""Abstract base provider — interface all AI providers must implement."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class EmbeddingResult:
    """Result from an embedding request."""
    embeddings: List[List[float]]
    model: str
    provider: str
    token_count: int
    cost_usd: float


@dataclass
class GenerationResult:
    """Result from a text generation request."""
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    prajna_scores: Optional[Dict[str, Any]] = field(default=None)


class BaseProvider(ABC):
    """Abstract base class for AI providers."""

    name: str = "base"

    @abstractmethod
    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        """Generate embeddings for a list of texts."""
        ...

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        """Generate text from a prompt."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is configured and available."""
        ...

    @abstractmethod
    async def health_check(self) -> dict:
        """Check provider health status."""
        ...
