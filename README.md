# KalevioAI 🛡

> **Detect the threat. File the NIS2 report. Automatically.**

KalevioAI is the only NIS2/DORA compliance platform that combines **live C2 threat detection** (ThreatFade engine) with **agentic AI report generation** — automating the full incident response workflow for European SMEs.

## The Problem

NIS2 Article 23 gives you **24 hours** to file an early warning after a significant incident. Most SMEs take days just to detect the incident. By then you are already in violation — with fines up to €10M or 2% of global turnover, and personal board liability.

## What KalevioAI Does

| Step | What Happens |
|---|---|
| **Detect** | ThreatFade analyses network traffic in real-time — validated against Merlin QUIC (Z=14.76), Cobalt Strike (Z=7.01), IcedID (Z=3.89) |
| **Classify** | AI agents determine NIS2/DORA reporting thresholds automatically |
| **Report** | Claude Sonnet 4.5 generates compliant incident reports — early warning, 72hr notification, 30-day final |
| **Notify** | One-click CSIRT submission across 27 EU member states |

## Why KalevioAI Wins

- ✅ **Only platform** combining live threat detection + compliance reporting
- ✅ **EU-native** — Estonian OÜ, EU data residency, CLOUD Act immune
- ✅ **6x cheaper** than Venvera (€49/mo vs €299/mo)
- ✅ **Four-layer LLM resilience** — Claude → Grok → Gemini → offline template
- ✅ **Hash-chained audit trail** — SHA-256, NIS2 5-year retention, tamper-proof
- ✅ **Open-source credibility** — PRs merged in Nuclei (24K⭐), TruffleHog (15K⭐), Semgrep (11K⭐)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| Frontend | Next.js 15 + TypeScript + Tailwind |
| Database | PostgreSQL 16 + pgvector + pgcrypto |
| Queue | Redis + Celery |
| AI Primary | Claude Sonnet 4.5 |
| AI Fallback | Grok-3 → Gemini 1.5 Flash → Offline template |
| Auth | Clerk (MFA + multi-tenancy) |
| Detection | ThreatFade v0.2.0-beta |
| Payments | LemonSqueezy |

## Quick Start

```bash
git clone https://github.com/Tinlance/kalevio
cd kalevio
cp .env.example .env
# Add your API keys to .env
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

API docs: `http://localhost:8000/api/docs`

## Test Suite

```bash
python -m pytest backend/tests/unit/ -v
# 26 passed, 0 failed
```

## Market

- **180,000+** EU organisations in NIS2/DORA scope
- **84%** not yet compliant
- **€10M** maximum fine per violation
- **October 2026** enforcement deadline
- **€13.4B** compliance automation market by 2034

## Compliance Coverage

| Framework | Status |
|---|---|
| NIS2 (EU) 2022/2555 | ✅ Article 21 — 10 measures |
| DORA (EU) 2022/2554 | ✅ 5 pillars |
| GDPR | 🔄 Sprint 2 |
| UK Cyber Resilience | 🔄 2027 |
| Australia Essential Eight | 🔄 2027 |

## License

Apache 2.0 — © 2026 [Tinlance OÜ](https://tinlance.com) · Tallinn, Estonia
