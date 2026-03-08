"""HuggingFace Provider — FREE embedding via Inference API."""

from typing import List, Optional
import httpx
from app.providers.base import BaseProvider, EmbeddingResult, GenerationResult
from app.config import settings


class HuggingFaceProvider(BaseProvider):
    """HuggingFace Inference API — FREE embeddings + generation."""

    name = "huggingface"
    # Updated endpoint — old api-inference.huggingface.co is 410 Gone
    BASE_URL = "https://router.huggingface.co/hf-inference"

    def __init__(self):
        self.api_key = getattr(settings, "huggingface_api_key", None) or ""
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def is_available(self) -> bool:
        return True

    async def embed(
        self, texts: List[str], model: Optional[str] = None
    ) -> EmbeddingResult:
        model = model or "sentence-transformers/all-MiniLM-L6-v2"
        url = f"{self.BASE_URL}/pipeline/feature-extraction/{model}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers=self.headers,
                json={"inputs": texts, "options": {"wait_for_model": True}},
            )
            response.raise_for_status()
            embeddings = response.json()

        est_tokens = sum(len(t.split()) for t in texts)

        return EmbeddingResult(
            embeddings=embeddings,
            model=model,
            provider=self.name,
            token_count=est_tokens,
            cost_usd=0.0,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> GenerationResult:
        model = model or "mistralai/Mistral-7B-Instruct-v0.3"
        url = f"{self.BASE_URL}/models/{model}"

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"[INST] {system_prompt}\n\n{prompt} [/INST]"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers=self.headers,
                json={
                    "inputs": full_prompt,
                    "parameters": {
                        "max_new_tokens": max_tokens,
                        "temperature": max(temperature, 0.01),
                        "return_full_text": False,
                    },
                },
            )
            response.raise_for_status()
            result = response.json()

        text = result[0]["generated_text"] if isinstance(result, list) else str(result)
        est_input = len(prompt.split())
        est_output = len(text.split())

        return GenerationResult(
            text=text,
            model=model,
            provider=self.name,
            input_tokens=est_input,
            output_tokens=est_output,
            cost_usd=0.0,
        )

    async def health_check(self) -> dict:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(
                    f"{self.BASE_URL}/models/sentence-transformers/all-MiniLM-L6-v2",
                    headers=self.headers,
                )
                if r.status_code == 200:
                    return {"status": "healthy", "cost": "FREE"}
                return {"status": "degraded", "reason": f"HTTP {r.status_code}"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
