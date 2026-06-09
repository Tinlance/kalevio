import asyncio, logging
from typing import Optional
import anthropic, httpx
from backend.core.config import settings

logger = logging.getLogger(__name__)

class LLMGateway:
    def __init__(self):
        self.claude = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def complete(self, prompt: str, system: Optional[str] = None, max_tokens: int = 2048) -> str:
        try:
            return await asyncio.wait_for(self._claude_complete(prompt, system, max_tokens), timeout=self.timeout)
        except Exception as e:
            logger.warning(f"Claude failed ({type(e).__name__}), switching to Grok")
            return await self._grok_complete(prompt, system, max_tokens)

    async def _claude_complete(self, prompt, system, max_tokens):
        kwargs = {"model": settings.LLM_PRIMARY, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}
        if system: kwargs["system"] = system
        r = await self.claude.messages.create(**kwargs)
        return r.content[0].text

    async def _grok_complete(self, prompt, system, max_tokens):
        async with httpx.AsyncClient() as client:
            msgs = []
            if system: msgs.append({"role": "system", "content": system})
            msgs.append({"role": "user", "content": prompt})
            r = await client.post("https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROK_API_KEY}"},
                json={"model": settings.LLM_FALLBACK, "messages": msgs, "max_tokens": max_tokens}, timeout=30.0)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

llm = LLMGateway()
