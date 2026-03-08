"""Together AI Provider — open source models at low cost."""

from typing import List, Optional
from openai import AsyncOpenAI
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.config import settings


class TogetherProvider(BaseProvider):
    """Together AI provider (OpenAI-compatible API)."""

    name = "together"

    def __init__(self):
        self.client = None
        if self.is_available():
            self.client = AsyncOpenAI(
                api_key=settings.together_api_key,
                base_url="https://api.together.xyz/v1",
            )

    def is_available(self) -> bool:
        return bool(settings.together_api_key)

    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        model = model or "BAAI/bge-large-en-v1.5"
        response = await self.client.embeddings.create(input=texts, model=model)
        embeddings = [item.embedding for item in response.data]
        total_tokens = response.usage.total_tokens

        # Pricing: ~$0.008/1M tokens
        cost = total_tokens * 0.008 / 1_000_000

        return EmbeddingResult(
            embeddings=embeddings,
            model=model,
            provider=self.name,
            token_count=total_tokens,
            cost_usd=cost,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        model = model or "meta-llama/Llama-3.3-70B-Instruct-Turbo"
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

        # Pricing: $0.88/1M in+out
        cost = (input_tokens + output_tokens) * 0.88 / 1_000_000

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
