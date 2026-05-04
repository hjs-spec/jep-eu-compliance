> **Exploratory mapping note. Not legal advice. Not part of JEP-Core.**
>
> This file describes possible JEP extension/profile fields for discussion only.

# Public Governance & Transparency Extension

**EU AI Act Reference**: Article 50 (transparency) + Article 52 (deepfakes) + Annex III (8) (justice/democratic processes, if applicable)  
**Risk Class**: Limited risk → High-risk boundary  
**JEP Industry Identifier**: `https://jep-eu-compliance mapping.org/industry/governance`

---

## Regulatory Context

AI systems interacting with citizens (chatbots, generative AI in public services, deepfakes) must comply with Article 50 transparency obligations from August 2, 2026. Public sector deployers of high-risk systems must also conduct FRIA (Art. 27).

Key obligations:
- Disclosure to users that they interact with AI (Art. 50(1))
- Labeling of synthetic content / deepfakes (Art. 50(2)(3))
- Machine-readable marking (Art. 50(4))
- Data minimization + right to be forgotten (GDPR overlap)
- FRIA for public sector high-risk deployment (Art. 27)

---

## JEP Primitive Mapping

| EU AI Act Requirement | JEP Verb | Semantics |
|-----------------------|----------|-----------|
| AI generates public response | J | `what` = hash of response + citizen request |
| Disclosure flag set | J | `disclosure_flag` in extension |
| Citizen requests human escalation | D | Delegation to human civil servant |
| Session closed / data anonymized | T | Termination with TTL trigger |
| Content authenticity verification | V | Verify synthetic content label |

---

## Extension Schema

```json
{
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/governance": {
      "disclosure_flag": true,
      "ai_interaction_notice_hash": "sha256:notice-text-hash",
      "citizen_request_hash": "sha256:anonymized-request-hash",
      "synthetic_content_label": false,
      "deepfake_flag": false,
      "machine_readable_mark": "c2pa:assertion-hash",
      "citizen_consent_hash": "sha256:consent-hash",
      "data_retention_policy": "gdpr_minimal",
      "ttl_expiry": 1750000000,
      "fria_reference": "fria-2026-045",
      "human_escalation_did": "did:example:tmp:civil-servant-001"
    }
  }
}
```

### Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `disclosure_flag` | boolean | True if AI interaction disclosed to user | Yes |
| `ai_interaction_notice_hash` | string | Hash of disclosure text | Yes |
| `citizen_request_hash` | string | Hash of citizen input (anonymized) | Yes |
| `synthetic_content_label` | boolean | True if output is AI-generated | Yes |
| `deepfake_flag` | boolean | True if synthetic media mimics real person | Yes |
| `machine_readable_mark` | string | C2PA or equivalent provenance mark | If synthetic |
| `citizen_consent_hash` | string | Hash of consent record | Yes |
| `data_retention_policy` | string | `gdpr_minimal`, `ai_act_6m`, `national_archive` | Yes |
| `ttl_expiry` | integer | Unix timestamp for auto-anonymization | Yes |
| `fria_reference` | string | FRIA ID if public sector high-risk | If applicable |
| `human_escalation_did` | string | DID of human civil servant | If escalation |

---

## Verification Strategy

1. **Signature & nonce** (JEP core)
2. **Disclosure check**: `disclosure_flag` MUST be true before J event `when`
3. **Synthetic content**: If `synthetic_content_label: true`, `machine_readable_mark` MUST be present
4. **Deepfake prohibition**: If `deepfake_flag: true` in prohibited context (Art. 5), event MUST be flagged for review
5. **TTL enforcement**: T event MUST trigger `ttl_expiry` anonymization; plaintext MUST NOT persist post-expiry
6. **Retention**: Per `data_retention_policy`; core hashes retained, plaintext anonymized

---

## Compliance Mapping Output Example

**Scenario**: Citizen uses public chatbot → AI discloses nature → Generates response → TTL set

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:gov-chatbot",
  "when": 1742345678,
  "what": "sha256:response-hash",
  "nonce": "uuid-401",
  "aud": "https://gov.example.com",
  "ref": null,
  "sig": "...",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/governance": {
      "disclosure_flag": true,
      "ai_interaction_notice_hash": "sha256:notice-hash",
      "citizen_request_hash": "sha256:request-hash",
      "synthetic_content_label": true,
      "machine_readable_mark": "c2pa:mark-hash",
      "citizen_consent_hash": "sha256:consent-hash",
      "data_retention_policy": "gdpr_minimal",
      "ttl_expiry": 1750000000
    }
  }
}
```

```json
{
  "jep": "1",
  "verb": "T",
  "who": "did:example:tmp:gov-chatbot",
  "when": 1742345680,
  "what": "sha256:session-close-hash",
  "nonce": "uuid-402",
  "aud": "https://gov.example.com",
  "ref": "sha256:response-hash",
  "sig": "...",
  "ext": {
    "https://jep.org/ttl": {
      "expiry": 1750000000,
      "expiry_policy": "anonymize_what"
    }
  }
}