"""Groq Provider — fastest LLM inference."""

from typing import List, Optional
from openai import AsyncOpenAI
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.config import settings


class GroqProvider(BaseProvider):
    """Groq API provider (OpenAI-compatible, blazing fast inference)."""

    name = "groq"

    def __init__(self):
        self.client = None
        if self.is_available():
            self.client = AsyncOpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            )

    def is_available(self) -> bool:
        return bool(settings.groq_api_key)

    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        raise NotImplementedError("Groq does not support embeddings. Use OpenAI or Google instead.")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        model = model or "llama-3.3-70b-versatile"
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
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        # Pricing: $0.59/1M in, $0.79/1M out
        cost = (input_tokens * 0.59 + output_tokens * 0.79) / 1_000_000

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
            return {"status": "unavailable", "reason": "No API key"}
        try:
            await self.client.models.list()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
