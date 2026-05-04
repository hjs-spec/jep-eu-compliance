> **Exploratory mapping note. Not legal advice. Not part of JEP-Core.**
>
> This file describes possible JEP extension/profile fields for discussion only.

# Medical Diagnosis Extension

**EU AI Act Reference**: Annex III (1)(a) + Annex I (MDR/IVDR, effective 2027-08-02)  
**Risk Class**: High-risk  
**JEP Industry Identifier**: `https://jep-eu-compliance mapping.org/industry/medical`

---

## Regulatory Context

AI systems used for medical diagnosis, triage, or treatment recommendation are classified as high-risk under Annex III (1)(a). When embedded in medical devices, Annex I obligations apply from August 2, 2027.

Key obligations:
- Risk management (Art. 9)
- Data governance with bias controls (Art. 10)
- Technical documentation per Annex IV (Art. 11)
- Automatic logging (Art. 12)
- Human oversight with override capability (Art. 14)
- Post-market monitoring (Art. 72)

---

## JEP Primitive Mapping

| EU AI Act Requirement | JEP Verb | Semantics |
|-----------------------|----------|-----------|
| AI initiates diagnosis | J | `what` = hash of diagnosis output + input data |
| Doctor reviews & confirms | D | Delegation to human clinician |
| Doctor overrides/rejects | T | Termination of AI decision lifecycle |
| Audit chain verification | V | Verify full J→D→T chain integrity |

---

## Extension Schema

```json
{
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/medical": {
      "diagnosis_code": "ICD-11:XXXX",
      "input_data_hash": "sha256:hash-of-imaging-or-lab-data",
      "confidence_score": 0.94,
      "human_review_required": true,
      "human_reviewer_did": "did:example:tmp:doctor-456",
      "model_version_hash": "sha256:hash-of-model-weights-manifest",
      "mdr_class": "IIa",
      "post_market_monitoring_id": "pm-2026-001"
    }
  }
}
```

### Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `diagnosis_code` | string | ICD-11 or SNOMED CT code | Yes |
| `input_data_hash` | string | Multihash of raw input (imaging, lab, EHR) | Yes |
| `confidence_score` | number | 0.0–1.0 model confidence | Yes |
| `human_review_required` | boolean | True for Annex III high-risk | Yes |
| `human_reviewer_did` | string | DID of reviewing clinician (ephemeral/salted) | If `human_review_required` |
| `model_version_hash` | string | Hash of model version manifest | Yes |
| `mdr_class` | string | MDR/IVDR classification (I, IIa, IIb, III) | If Annex I applicable |
| `post_market_monitoring_id` | string | Reference to PMS plan (Art. 72) | Yes |

---

## Verification Strategy

1. **Signature validity** (JEP core)
2. **Nonce uniqueness** (JEP core)
3. **Chain integrity**: Root J event must have `ref: null` + `task_based_on: null`
4. **Human oversight check**: If `human_review_required: true`, chain MUST contain D or T event with matching `human_reviewer_did`
5. **Model traceability**: `model_version_hash` must be registered in EU database (Art. 49)
6. **Retention**: 6 months minimum (Art. 26) + 10 years technical documentation (Art. 11)

---

## Compliance Mapping Output Example

**Scenario**: AI suggests diagnosis → Doctor confirms → Treatment proceeds

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:ai-diagnostic-agent",
  "when": 1742345678,
  "what": "sha256:diagnosis-output-hash",
  "nonce": "uuid-001",
  "aud": "https://hospital.example.com",
  "ref": null,
  "sig": "...",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/medical": {
      "diagnosis_code": "ICD-11:2A00",
      "input_data_hash": "sha256:ct-scan-hash",
      "confidence_score": 0.94,
      "human_review_required": true,
      "model_version_hash": "sha256:model-v3.2"
    }
  }
}
```

```json
{
  "jep": "1",
  "verb": "D",
  "who": "did:example:tmp:doctor-456",
  "when": 1742345680,
  "what": "sha256:approval-signature-hash",
  "nonce": "uuid-002",
  "aud": "https://hospital.example.com",
  "ref": "sha256:diagnosis-output-hash",
  "sig": "...",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/medical": {
      "human_reviewer_did": "did:example:tmp:doctor-456",
      "override_reason": null
    }
  }
}
```

---

## Post-Market Monitoring Integration

Per Art. 72, deployers MUST establish continuous monitoring. JEP supports this via periodic V events:

```json
{
  "verb": "V",
  "what": null,
  "ref": "sha256:original-j-event-hash",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/medical": {
      "monitoring_type": "post_market",
      "adverse_event_flag": false,
      "performance_drift_detected": false
    }
  }
}