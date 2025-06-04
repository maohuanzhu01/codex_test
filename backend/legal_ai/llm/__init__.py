from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .client import get_llm_client, LLMClient


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"

_env = Environment(loader=FileSystemLoader(str(PROMPTS_DIR)))


def _extract_citations(text: str) -> list[str]:
    """Extract citation ids from output text."""
    return sorted(set(re.findall(r"\[(\d+)\]", text)))


def generate_response(
    question: str,
    context: str = "",
    client_kind: str = "openai",
) -> tuple[str, list[str]]:
    """Render prompt and get completion from chosen LLM.

    Returns a tuple ``(text, cited_ids)``.
    """
    template = _env.get_template("base.jinja2")
    prompt = template.render(question=question, context=context)

    client: LLMClient = get_llm_client(client_kind)
    text = client.generate(prompt)
    cited_ids = _extract_citations(text)
    return text, cited_ids
