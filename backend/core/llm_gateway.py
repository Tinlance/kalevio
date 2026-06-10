"""
KalevioAI LLM Gateway — Four-Layer Resilience
Layer 1: Claude Sonnet 4.5 (primary)
Layer 2: Grok-3 (fallback)
Layer 3: Gemini 1.5 Flash (emergency)
Layer 4: Template fallback (offline — always works)
"""
import asyncio
import logging
from typing import Optional
import anthropic
import httpx
from backend.core.config import settings

logger = logging.getLogger(__name__)

NIS2_TEMPLATE = """
NIS2 ARTICLE 23 INCIDENT REPORT — AUTO-GENERATED
Incident Reference: {reference_id}
Report Type: {report_type}
Generated: {timestamp}
Framework: NIS2 Directive (EU) 2022/2555

SECTION 1 — INCIDENT DESCRIPTION
Threat detected: {threat_type}
Detection time: {detected_at}
Severity: {severity}
Affected systems: {affected_systems}

SECTION 2 — INITIAL ASSESSMENT
Anomaly score (Z): {z_score}
MITRE ATT&CK TTPs: {mitre_ttps}
Cross-border impact: Under assessment

SECTION 3 — MEASURES TAKEN
Immediate isolation applied. Investigation ongoing.

SECTION 4 — REGULATORY COMPLIANCE
Early warning: NIS2 Article 23(1)(a) — 24 hours
Full notification to follow within 72 hours per Article 23(1)(b).

NOTE: Generated via offline template — AI unavailable. Human review required.
"""

class LLMGateway:
    def __init__(self):
        self.claude = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def complete(self, prompt: str, system: Optional[str] = None,
                       max_tokens: int = 2048, template_data: Optional[dict] = None) -> tuple:
        # Layer 1 — Claude
        try:
            content = await self._claude_complete(prompt, system, max_tokens)
            logger.info("LLM: Claude Sonnet 4.5")
            return content, "claude-sonnet-4-5"
        except Exception as e:
            logger.warning(f"Claude failed: {type(e).__name__}")

        # Layer 2 — Grok
        try:
            content = await asyncio.wait_for(
                self._grok_complete(prompt, system, max_tokens), timeout=self.timeout)
            logger.info("LLM: Grok-3 fallback")
            return content, "grok-3"
        except Exception as e:
            logger.warning(f"Grok failed: {type(e).__name__}")

        # Layer 3 — Gemini
        try:
            content = await asyncio.wait_for(
                self._gemini_complete(prompt, max_tokens), timeout=self.timeout)
            logger.info("LLM: Gemini Flash emergency fallback")
            return content, "gemini-2.0-flash"
        except Exception as e:
            logger.warning(f"Gemini failed: {type(e).__name__} — using template")

        # Layer 4 — Offline template (never fails)
        logger.error("All LLM layers failed — offline template")
        data = template_data or {
            "reference_id": "PENDING", "report_type": "early_warning",
            "timestamp": "See logs", "threat_type": "Under investigation",
            "detected_at": "See logs", "severity": "Under assessment",
            "affected_systems": "Under investigation",
            "z_score": "N/A", "mitre_ttps": "Under analysis",
        }
        return NIS2_TEMPLATE.format(**data), "offline-template"

    async def _claude_complete(self, prompt, system, max_tokens):
        kwargs = {"model": settings.LLM_PRIMARY, "max_tokens": max_tokens,
                  "messages": [{"role": "user", "content": prompt}]}
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
                json={"model": "grok-3", "messages": msgs, "max_tokens": max_tokens},
                timeout=30.0)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

    async def _gemini_complete(self, prompt, max_tokens):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}",
                json={"contents": [{"parts": [{"text": prompt}]}],
                      "generationConfig": {"maxOutputTokens": max_tokens}},
                timeout=30.0)
            r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]

llm = LLMGateway()
