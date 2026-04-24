---
tags:
- ai-governance
- eu-ai-act
- compliance
- audit-trail
- jep
- accountability
- transparency
- event-logging
- markdown
license: cc0-1.0
language:
- en
- zh
size_categories:
- n<1K
---

# JEP EU Multi-Industry Compliance Extensions

**Repository**: `cognitiveemergencelab/jep-eu-compliance`  
**License**: CC0 1.0 Universal — JEP belongs to the public domain.  
**Version**: 1.0.0  
**Date**: 2026-04-24

---

## One Grammar, All Industries

JEP Core (J/D/T/V) is immutable. Industry differences are expressed only through:
- `what_content` semantics
- Optional extension fields
- Verification thresholds

This repository provides EU AI Act (Regulation (EU) 2024/1689) compliance mappings for six high-risk sectors under Annex III and Article 50, effective **August 2, 2026**.

---

## EU AI Act Timeline (Relevant to This Repo)

| Date | Milestone |
|------|-----------|
| 2025-02-02 | Prohibited practices & AI literacy (Art. 4, 5) — in force |
| 2025-08-02 | GPAI obligations & governance — in force |
| **2026-08-02** | **High-risk systems (Annex III) & transparency (Art. 50)** |
| 2027-08-02 | High-risk in regulated products (Annex I): medical devices, machinery, vehicles |

> **Warning**: The Digital Omnibus proposes postponing Annex III to December 2027, but this is **not enacted law**. Treat August 2, 2026 as binding.

---

## Penalty Framework

| Violation | Fine |
|-----------|------|
| Prohibited practices (Art. 5) | Up to €35M or 7% global turnover |
| High-risk obligations (Art. 9–17, 26) | Up to €15M or 3% global turnover |
| Transparency (Art. 50) | Up to €7.5M or 1% global turnover |

---

## Repository Structure

```
jep-eu-compliance/
├── README.md
├── EU_AI_ACT_MAPPING.md          # Regulation article ↔ JEP primitive mapping
├── DISCLAIMER.md                 # Legal disclaimer (MUST READ)
└── extensions/
    ├── medical.md                # Annex I + III (biometrics/diagnosis)
    ├── fintech.md                # Annex III (5)(b) — credit scoring
    ├── automotive.md             # Annex III (2) — traffic safety
    ├── hr.md                     # Annex III (4)(a) — recruitment
    ├── governance.md             # Art. 50 — chatbots, deepfakes, public service
    └── critical-infra.md         # Annex III (2) — energy, water, transport
```

---

## Core Principle: Narrow Waist

**JEP Core never changes across industries:**

| Verb | Universal Meaning |
|------|-------------------|
| J (Judge) | AI initiates a decision |
| D (Delegate) | Authority transferred to human or another agent |
| T (Terminate) | Decision lifecycle closed — human override, completion, or rejection |
| V (Verify) | Cryptographic verification of any event in the chain |

All EU AI Act requirements map into this semantic space without altering the core grammar.

---

## Quick Start

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:agent-123",
  "when": 1742345678,
  "what": "sha256:hash-of-decision-content",
  "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "aud": "https://platform.example.com",
  "ref": null,
  "sig": "eyJhbGciOiJFZERTQSJ9...",
  "extensions": {
    "https://jep.org/priv/digest-only": {
      "identity_digest": "sha256:...",
      "salt_provider": "did:example:trusted-anchor"
    },
    "https://jep-eu-compliance.org/industry": "medical",
    "https://jep-eu-compliance.org/risk-class": "high",
    "https://jep-eu-compliance.org/art-ref": "Annex-III-1a"
  }
}
```

---

## Compliance Coverage Matrix

| EU AI Act Requirement | JEP Primitive | Extension | Industry Coverage |
|-----------------------|-------------|-----------|-------------------|
| Automatic logging (Art. 12) | J/D/T/V + `what` hash | — | All |
| Human oversight (Art. 14) | D (Delegate) / T (Terminate) | `human_override` flag | All |
| Transparency (Art. 50) | V (Verify) + `disclosure_flag` | `governance` | Governance |
| Risk management (Art. 9) | J chain + `risk_level` | `risk` | All |
| Data minimization / TTL | T (Terminate) | `https://jep.org/ttl` | All |
| 6-month log retention | — | `retention_policy` | All |
| FRIA (Art. 27) | J chain root | `fria_reference` | Public sector |

---

## Legal Disclaimer

**JEP provides technical audit infrastructure, not legal advice.**  
See `DISCLAIMER.md` for full text.

> "JEP provides auditable event records. Legal compliance depends on deployment-specific configuration and regulatory interpretation."

---

## Author

Yuqiang Wang | yuqiang@humanjudgment.org | https://humanjudgment.org
```