import os
from typing import Protocol

class LLMClient(Protocol):
    """Simple protocol for LLM clients."""

    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError


class OpenAIClient:
    """Client for OpenAI's chat completion API."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            import openai
        except ImportError as exc:
            raise RuntimeError("openai package is required for OpenAIClient") from exc

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()


class LocalHFClient:
    """Client that uses a local HuggingFace pipeline."""

    def __init__(self, model: str = "distilgpt2"):
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError("transformers package is required for LocalHFClient") from exc

        self.generator = pipeline("text-generation", model=model)

    def generate(self, prompt: str) -> str:
        outputs = self.generator(prompt, max_length=256, num_return_sequences=1)
        return outputs[0]["generated_text"].strip()


def get_llm_client(kind: str = "openai") -> LLMClient:
    """Factory that returns the desired LLM client."""
    if kind == "openai":
        return OpenAIClient()
    if kind == "local":
        return LocalHFClient()
    raise ValueError(f"Unsupported LLM client: {kind}")
