---
tags:
- jep
- eu-ai-act
- ai-governance
- compliance-mapping
- research
- not-legal-advice
- audit-trail
- ai-accountability
license: mit
language:
- en
size_categories:
- n<1K
---

# JEP EU AI Act Mapping Notes

> **Exploratory / Not Legal Advice**
>
> This repository contains exploratory EU AI Act mapping notes for JEP.
> It is not legal advice, not a compliance guarantee, and not part of JEP-Core.
>
> Official EU AI Act materials, regulator guidance, and qualified legal counsel should always take precedence.

---

## Current Protocol Context

Current public version line:

| Layer | Current Version | Repository |
|---|---|---|
| JEP | v0.6 | https://github.com/hjs-spec/jep-v06 |
| JEP API | v0.6 | https://github.com/hjs-spec/jep-api |
| HJS | v0.5 | https://github.com/hjs-spec/hjs-05 |
| JAC | v0.5 | https://github.com/hjs-spec/jac-agent-02 |

Public drafts:

- JEP-Core: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP-Profiles: https://datatracker.ietf.org/doc/draft-wang-jep-profiles/
- JEP-Conformance: https://datatracker.ietf.org/doc/draft-wang-jep-conformance/
- HJS: https://datatracker.ietf.org/doc/draft-wang-hjs-accountability/
- JAC: https://datatracker.ietf.org/doc/draft-wang-jac/

---

## Repository Role

This repository provides exploratory mappings between JEP-style event records and selected EU AI Act auditability, transparency, traceability, and documentation concepts.

It is intended for:

- research discussion;
- scenario analysis;
- industry mapping experiments;
- audit-trail design exploration;
- JEP extension-profile discussion.

It is **not**:

- a legal compliance product;
- a compliance certification;
- a legal opinion;
- a normative part of JEP-Core;
- the JEP v0.6 conformance suite;
- a guarantee that a system complies with the EU AI Act.

---

## Core Principle

JEP-Core remains a narrow event layer.

Industry-specific or regulatory mappings should be expressed through optional profiles or extensions, without changing the JEP-Core grammar.

```text
JEP-Core = signed judgment events
EU mapping notes = optional external interpretation / deployment guidance
```

JEP can provide technical event records that may support auditability, traceability, transparency, documentation, or review workflows.

JEP does not itself determine legal compliance.

---

## JEP v0.6 Extension Style

Examples in this repository use the JEP v0.6 extension structure:

```json
{
  "ext": {
    "https://jep-eu-compliance.org/industry": "medical",
    "https://jep-eu-compliance.org/risk-class": "high",
    "https://jep-eu-compliance.org/art-ref": "Annex-III-1a"
  },
  "ext_crit": []
}
```

Older examples using `extensions` should be treated as historical.

---

## Repository Structure

```text
README.md
DISCLAIMER.md
LEGAL-STATUS.md
EU_AI_ACT_MAPPING.md
NOTICE.md
LICENSE

examples/
  automotive_j.json
  critical-infra_j.json
  fintech_j.json
  governance_j.json
  hr_j.json
  medical_j.json

extensions/
  critical-infra.md
  fintech.md
  governance.md
  hr.md
  medical.md

schemas/
  automotive.schema.json
  critical-infra.schema.json
  fintech.schema.json
  governance.schema.json
  hr.schema.json
  medical.schema.json

implementations/
  verify_jep_eu.py
  test_verify_jep_eu.py
```

---

## Mapping Categories

The repository includes exploratory notes for:

- medical and health-related contexts;
- fintech and credit-related contexts;
- automotive and transport contexts;
- human resources contexts;
- governance and public-service contexts;
- critical infrastructure contexts.

These are mapping notes, not compliance determinations.

---

## Legal Status

See:

```text
LEGAL-STATUS.md
DISCLAIMER.md
```

The EU AI Act has staged application dates and may be affected by later regulatory, delegated, implementing, or guidance materials.

This repository may become outdated.

---

## Boundary Statement

A JEP event can record that an actor made, delegated, terminated, or verified a claim.

It does not prove:

- the claim is true;
- the system is compliant;
- human oversight was legally sufficient;
- documentation was complete;
- risk management was adequate;
- a legal obligation was satisfied.

Those determinations require external legal, organizational, technical, and regulatory review.

---

## Public Resources

- JEP v0.6 Repository: https://github.com/hjs-spec/jep-v06
- JEP API v0.6 Repository: https://github.com/hjs-spec/jep-api
- HJS v0.5 Repository: https://github.com/hjs-spec/hjs-05
- JAC v0.5 Repository: https://github.com/hjs-spec/jac-agent-02
- JEP v0.6 Spec Demo: https://huggingface.co/spaces/yuqiangJEP/jep-v06-spec-demo/tree/main
- JEP v0.6 Conformance Suite: https://huggingface.co/datasets/yuqiangJEP/jep-v06-conformance-suite

---

## License and Legal Notice

Implementation examples, schemas, and mapping notes are provided under the repository license unless otherwise stated.

Internet-Draft text and excerpts, if present, are governed by the IETF Trust Legal Provisions and BCP 78 / BCP 79.

See `NOTICE.md`.
