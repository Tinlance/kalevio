<div align="center">

<img src="https://img.shields.io/badge/KalevioAI-NIS2%2FDORA%20Copilot-2b7fff?style=for-the-badge&logo=shield&logoColor=white" alt="KalevioAI"/>

<h3>Detect the threat. File the NIS2 report. Automatically.</h3>

<p>The only compliance platform that combines live C2 threat detection with agentic AI report generation — for European SMEs facing the October 2026 NIS2 deadline.</p>

[![CI](https://github.com/Tinlance/kalevio/actions/workflows/ci.yml/badge.svg)](https://github.com/Tinlance/kalevio/actions)
[![Tests](https://img.shields.io/badge/tests-26%20passed-00d68f?style=flat-square)](https://github.com/Tinlance/kalevio/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![NIS2](https://img.shields.io/badge/NIS2-Article%2021%20%E2%9C%93-2b7fff?style=flat-square)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555)
[![DORA](https://img.shields.io/badge/DORA-5%20Pillars%20%E2%9C%93-ffaa00?style=flat-square)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554)
[![Made in Estonia](https://img.shields.io/badge/Made%20in-Estonia%20%F0%9F%87%AA%F0%9F%87%AA-black?style=flat-square)](https://tinlance.com)

</div>

---

## The Problem

NIS2 Article 23 gives you **24 hours** to file an early warning after a significant incident. Most SMEs take days just to detect the incident. By then you are already in violation — fines up to **€10M or 2% of global turnover**, with **personal board liability**.

Every existing tool solves half the problem. Security tools detect threats but don't generate compliance reports. Compliance tools generate reports but don't detect threats. KalevioAI does both in one automated flow.

---

## How It Works
| Step | What Happens | Technology |
|------|-------------|------------|
| **Detect** | Real-time C2 detection — Merlin QUIC Z=14.76, Cobalt Strike Z=7.01 | ThreatFade v0.2 |
| **Classify** | NIS2/DORA threshold evaluation, severity scoring | FastAPI + Python |
| **Report** | AI-generated Article 23 incident reports | Claude Sonnet 4.5 |
| **Notify** | One-click CSIRT submission, board alerts | Resend + 27 CSIRTs |

---

## Why KalevioAI Wins

| Feature | Venvera | Orbiq | Heimdal | **KalevioAI** |
|---------|---------|-------|---------|--------------|
| NIS2/DORA native | ✅ | ✅ | ⚠️ | ✅ |
| Live threat detection | ❌ | ❌ | ⚠️ | ✅ **ThreatFade** |
| AI report generation | ⚠️ | ⚠️ | ❌ | ✅ **Claude 4.5** |
| Auto CSIRT notify | ❌ | ❌ | ❌ | ✅ **27 states** |
| Hash-chained audit | ⚠️ | ⚠️ | ⚠️ | ✅ **SHA-256** |
| EU data residency | ✅ | ✅ | ✅ | ✅ **Estonia** |
| Starting price | €299/mo | N/A | N/A | **€49/mo** |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Python 3.12 |
| Frontend | Next.js 15 + TypeScript + Tailwind CSS |
| Database | PostgreSQL 16 + pgvector + pgcrypto |
| Queue | Redis + Celery |
| AI Primary | Claude Sonnet 4.5 |
| AI Fallback | Grok-3 → Gemini 1.5 Flash → Offline template |
| Auth | Clerk (MFA + multi-tenancy + RLS) |
| Detection | ThreatFade v0.2.0-beta |
| Payments | LemonSqueezy (EU VAT auto-handled) |
| Email | Resend |
| Monitoring | Sentry + PostHog + BetterUptime |

---

## Quick Start

```bash
git clone https://github.com/Tinlance/kalevio
cd kalevio
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

API docs: `http://localhost:8000/api/docs`

### API Example

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Check NIS2 scope
curl http://localhost:8000/api/v1/compliance/scope-check

# Create incident (auto-sets 24h/72h/30d NIS2 deadlines)
curl -X POST http://localhost:8000/api/v1/incidents/ \
  -H "Content-Type: application/json" \
  -d '{"threat_type": "Merlin QUIC C2", "z_score": 14.76, "mitre_ttps": ["T1071.001", "T1027"]}'
```

---

## Tests

```bash
python -m pytest backend/tests/unit/ -v
# 26 passed, 0 failed in 0.99s
```

**Test coverage:**
- ThreatFade engine — Z-score, MITRE mapping, confidence bounds
- NIS2 Article 21 — 10 measures, weights sum to 100, CSIRT endpoints
- Hash-chained audit log — SHA-256 determinism, tamper detection
- NIS2 deadlines — 24h/72h/30d precision, severity classification

---

## Compliance Coverage

| Framework | Region | Status | Sprint |
|-----------|--------|--------|--------|
| NIS2 (EU) 2022/2555 — Article 21 | 🇪🇺 EU | ✅ Live | Sprint 1 |
| DORA (EU) 2022/2554 — 5 Pillars | 🇪🇺 EU | ✅ Live | Sprint 1 |
| GDPR Article 30 + 32 | 🇪🇺 EU | 🔄 Sprint 2 | Sprint 2 |
| UK Cyber Security & Resilience Bill | 🇬🇧 UK | 📋 Planned | 2027 |
| Australia Essential Eight | 🇦🇺 AU | 📋 Planned | 2027 |
| ISO 27001 | 🌍 Global | 📋 Planned | 2027 |

### CSIRT Coverage (27 EU Member States)

Pre-built notification templates for: 🇪🇪 EE · 🇩🇪 DE · 🇳🇱 NL · 🇧🇪 BE · 🇫🇷 FR · 🇵🇱 PL · 🇸🇪 SE · 🇮🇹 IT · 🇪🇸 ES · 🇮🇪 IE + 17 more

---

## Roadmap

### ✅ Sprint 1 — Foundation (Complete)
- [x] FastAPI backend + 8 routers
- [x] PostgreSQL models + pgvector
- [x] ThreatFade v0.2 integration
- [x] NIS2 Article 21 compliance engine
- [x] DORA 5-pillar framework
- [x] SHA-256 hash-chained audit log
- [x] Four-layer LLM gateway (Claude → Grok → Gemini → template)
- [x] 26 unit tests passing
- [x] CI/CD GitHub Actions

### 🔄 Sprint 2 — Core Product (In Progress)
- [ ] NIS2 Scope Checker wizard (5-question flow)
- [ ] Compliance scoring engine (0-100%)
- [ ] Incident Report Agent (LangChain + Claude)
- [ ] Celery PCAP processing queue
- [ ] Evidence vault (file upload)
- [ ] Board-level management dashboard
- [ ] Clerk auth + multi-tenancy

### 📋 Sprint 3 — Revenue (Q3 2026)
- [ ] LemonSqueezy billing (Free/€49/€199)
- [ ] MS365 + Google Workspace + AWS integrations
- [ ] Supply chain vendor risk module
- [ ] Public Trust Center page
- [ ] Landing page live at kalevioai.com

### 🌍 2027 — Global Expansion
- [ ] UK Cyber Security & Resilience Bill module
- [ ] Australia Essential Eight module
- [ ] ISO 27001 module
- [ ] MSSP/reseller channel

---

## Self-Hosting

KalevioAI is fully self-hostable for organisations with strict EU data sovereignty requirements.

```bash
# Docker Compose (coming Sprint 2)
docker compose up -d

# Manual
cp .env.example .env
# Configure DATABASE_URL, REDIS_URL, and API keys
pip install -r backend/requirements.txt
alembic upgrade head
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

All incident data, reports, and audit logs remain on your infrastructure. No data leaves your environment without explicit CSIRT submission.

---

## Market

- **180,000+** EU organisations in NIS2/DORA scope
- **84%** not yet compliant (CyberSmart, 2025 — 670 business leaders surveyed)
- **€10M** maximum fine per NIS2 violation
- **October 2026** active enforcement deadline
- **€13.4B** compliance automation market by 2034 (16.4% CAGR)

---

## Security

We take security seriously — this is a security product.

**Responsible Disclosure:** Found a vulnerability? Please email `security@kalevioai.com`. We respond within 48 hours and follow coordinated disclosure practices. Do not open a public GitHub issue for security vulnerabilities.

**Security practices in this codebase:**
- All audit entries are SHA-256 hash-chained — tampering is detectable
- Secrets never committed — `.env` in `.gitignore`, `.env.example` provided
- Rate limiting on all endpoints via `slowapi`
- LemonSqueezy webhook signature verification
- Clerk JWT verification on all protected routes (Sprint 2)

---

## Contributing

We welcome contributions — especially from the EU security and compliance community.

```bash
# Fork, clone, create branch
git checkout -b feature/your-feature

# Run tests before any PR
python -m pytest backend/tests/unit/ -v

# All tests must pass — no exceptions
# Add tests for any new functionality
```

**Good first issues:** Look for issues labelled `good first issue` — CSIRT endpoint additions, compliance framework mappings, and translation help are always welcome.

**Code of Conduct:** Be professional. This project serves organisations facing real regulatory deadlines.

---

## About

Built by [Chinaemerem Nwachukwu (LloydCoder)](https://github.com/LloydCoder) — founder of [Tinlance Limited](https://tinlance.com) (RC: 7962164, Nigeria) and Tinlance OÜ (Estonia).

**Open-source credibility:** PRs merged in [Nuclei](https://github.com/projectdiscovery/nuclei) (24K⭐), [TruffleHog](https://github.com/trufflesecurity/trufflehog) (15K⭐), [Semgrep](https://github.com/returntocorp/semgrep) (11K⭐), [Gitleaks](https://github.com/gitleaks/gitleaks) (10K⭐), [Slither](https://github.com/crytic/slither) (5K⭐)

---

## License

Apache 2.0 — © 2026 Tinlance OÜ · Tallinn, Estonia

See [LICENSE](LICENSE) for full terms.
