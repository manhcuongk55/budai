"""Google Gemini Provider — embeddings + generation via Google AI."""

from typing import List, Optional
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.config import settings

try:
    from google import genai
    from google.genai import types
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False


class GoogleProvider(BaseProvider):
    """Google Gemini API provider."""

    name = "google"

    def __init__(self):
        self.client = None
        if self.is_available():
            self.client = genai.Client(api_key=settings.google_api_key)

    def is_available(self) -> bool:
        return bool(settings.google_api_key) and HAS_GOOGLE

    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        model = model or "text-embedding-004"
        result = self.client.models.embed_content(
            model=model,
            contents=texts,
        )

        embeddings = [list(e.values) for e in result.embeddings]
        # Estimate tokens (~4 chars per token)
        total_chars = sum(len(t) for t in texts)
        est_tokens = total_chars // 4

        # Pricing: ~$0.006/1M tokens
        cost = est_tokens * 0.006 / 1_000_000

        return EmbeddingResult(
            embeddings=embeddings,
            model=model,
            provider=self.name,
            token_count=est_tokens,
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
        model = model or "gemini-2.5-flash"

        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        if system_prompt:
            config.system_instruction = system_prompt

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        text = response.text
        input_tokens = response.usage_metadata.prompt_token_count or 0
        output_tokens = response.usage_metadata.candidates_token_count or 0

        # Pricing: gemini-2.5-flash ~$0.10/1M in, $0.40/1M out
        cost = (input_tokens * 0.10 + output_tokens * 0.40) / 1_000_000

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
            return {"status": "unavailable", "reason": "No API key or google-genai not installed"}
        try:
            self.client.models.list()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
