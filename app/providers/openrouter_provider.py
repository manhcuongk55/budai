"""OpenRouter Provider — FREE access to many LLMs."""

from typing import List, Optional
from openai import AsyncOpenAI
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.config import settings


class OpenRouterProvider(BaseProvider):
    """OpenRouter — aggregates many LLMs, some FREE."""

    name = "openrouter"

    # Free models on OpenRouter (no API key needed for some)
    FREE_MODELS = [
        "google/gemma-3-1b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen3-0.6b:free",
    ]

    def __init__(self):
        self.api_key = getattr(settings, "openrouter_api_key", None)
        self.client = None
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={"HTTP-Referer": "https://budai.app", "X-Title": "budAI"},
            )

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        raise NotImplementedError("OpenRouter does not support embeddings. Use HuggingFace instead.")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        # Default to free model
        model = model or self.FREE_MODELS[0]
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        text = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens if response.usage else len(prompt.split())
        output_tokens = response.usage.completion_tokens if response.usage else len(text.split())

        # Free models = $0
        is_free = ":free" in model
        cost = 0.0 if is_free else (input_tokens * 0.15 + output_tokens * 0.60) / 1_000_000

        return GenerationResult(
            text=text,
            model=model,
            provider=self.name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )

    async def health_check(self) -> dict:
        if not self.is_available():
            return {"status": "unavailable", "reason": "No API key (get free at openrouter.ai)"}
        try:
            await self.client.models.list()
            return {"status": "healthy", "cost": "FREE models available"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
