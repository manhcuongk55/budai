"""Smart Cost Router — the heart of budAI's cost optimization."""

import logging
from typing import Dict, List, Optional
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.providers.openai_provider import OpenAIProvider
from app.providers.google_provider import GoogleProvider
from app.providers.deepseek_provider import DeepSeekProvider
from app.providers.groq_provider import GroqProvider
from app.providers.together_provider import TogetherProvider
from app.providers.huggingface_provider import HuggingFaceProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.optimizer.pricing import (
    TaskType,
    Strategy,
    get_models_by_task,
    ModelPricing,
)
from app.config import settings

logger = logging.getLogger("budai.router")


class CostRouter:
    """
    Smart router that selects the cheapest/fastest/best AI provider.
    Auto-failover: if a provider fails, try the next one.
    """

    def __init__(self):
        self.providers: Dict[str, BaseProvider] = {}
        self._init_providers()

    def _init_providers(self):
        """Initialize all available providers."""
        all_providers = [
            HuggingFaceProvider(),   # FREE — always available
            OpenAIProvider(),
            GoogleProvider(),
            DeepSeekProvider(),
            GroqProvider(),
            TogetherProvider(),
            OpenRouterProvider(),
        ]
        for provider in all_providers:
            if provider.is_available():
                self.providers[provider.name] = provider
                logger.info(f"✅ Provider '{provider.name}' is available")
            else:
                logger.warning(f"⚠️  Provider '{provider.name}' not configured (no API key)")

        if not self.providers:
            logger.error("❌ No providers available! Add at least one API key to .env")

    def _rank_providers(
        self,
        task_type: TaskType,
        strategy: Strategy = Strategy.CHEAPEST,
    ) -> List[ModelPricing]:
        """Rank available models by strategy."""
        models = get_models_by_task(task_type)

        # Filter to only available providers
        available = [m for m in models if m.provider in self.providers]

        if not available:
            raise ValueError(
                f"No providers available for {task_type.value}. "
                f"Available providers: {list(self.providers.keys())}"
            )

        if strategy == Strategy.CHEAPEST:
            return sorted(available, key=lambda m: m.input_cost_per_million)
        elif strategy == Strategy.FASTEST:
            return sorted(available, key=lambda m: m.avg_latency_ms)
        elif strategy == Strategy.BEST:
            return sorted(available, key=lambda m: m.quality_score, reverse=True)

        return available

    async def embed(
        self,
        texts: List[str],
        strategy: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> EmbeddingResult:
        """
        Generate embeddings using the optimal provider.

        Args:
            texts: List of texts to embed
            strategy: cheapest|fastest|best (default from config)
            provider: Force a specific provider
            model: Force a specific model
        """
        strat = Strategy(strategy or settings.default_strategy)

        if provider and provider in self.providers:
            return await self.providers[provider].embed(texts, model)

        # Try providers in ranked order (auto-failover)
        ranked = self._rank_providers(TaskType.EMBEDDING, strat)
        last_error = None

        for model_info in ranked:
            try:
                p = self.providers[model_info.provider]
                result = await p.embed(texts, model_info.model)
                logger.info(
                    f"🙏 Embed via {model_info.provider}/{model_info.model} "
                    f"— {result.token_count} tokens, ${result.cost_usd:.6f}"
                )
                return result
            except NotImplementedError:
                continue
            except Exception as e:
                last_error = e
                logger.warning(
                    f"⚠️  {model_info.provider} failed: {e}. Trying next..."
                )
                continue

        raise RuntimeError(f"All embedding providers failed. Last error: {last_error}")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        strategy: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        """
        Generate text using the optimal provider.

        Args:
            prompt: User prompt
            system_prompt: System instruction
            strategy: cheapest|fastest|best
            provider: Force a specific provider
            model: Force a specific model
        """
        strat = Strategy(strategy or settings.default_strategy)

        if provider and provider in self.providers:
            return await self.providers[provider].generate(
                prompt, system_prompt, model, max_tokens, temperature
            )

        ranked = self._rank_providers(TaskType.GENERATION, strat)
        last_error = None

        for model_info in ranked:
            try:
                p = self.providers[model_info.provider]
                result = await p.generate(
                    prompt, system_prompt, model_info.model, max_tokens, temperature
                )
                logger.info(
                    f"🙏 Generate via {model_info.provider}/{model_info.model} "
                    f"— {result.input_tokens}+{result.output_tokens} tokens, "
                    f"${result.cost_usd:.6f}"
                )
                return result
            except NotImplementedError:
                continue
            except Exception as e:
                last_error = e
                logger.warning(
                    f"⚠️  {model_info.provider} failed: {e}. Trying next..."
                )
                continue

        raise RuntimeError(f"All generation providers failed. Last error: {last_error}")

    async def get_status(self) -> Dict:
        """Get status of all providers."""
        status = {}
        for name, provider in self.providers.items():
            status[name] = await provider.health_check()
        return status

    def list_providers(self) -> List[str]:
        """List available provider names."""
        return list(self.providers.keys())


# Singleton router instance
router = CostRouter()
