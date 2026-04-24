# Recruitment & HR Extension

**EU AI Act Reference**: Annex III (4)(a) — Employment, worker management, access to self-employment  
**Risk Class**: High-risk  
**JEP Industry Identifier**: `https://jep-eu-compliance.org/industry/hr`

---

## Regulatory Context

AI systems used for recruitment, selection, or performance evaluation are high-risk under Annex III (4)(a). These systems carry significant discrimination risk and require robust audit trails for equal opportunity litigation.

Key obligations:
- Data governance with bias mitigation (Art. 10)
- Human oversight with final decision authority (Art. 14)
- Transparency to candidates (Art. 13)
- Automatic logging (Art. 12)
- FRIA if public sector employer (Art. 27)

---

## JEP Primitive Mapping

| EU AI Act Requirement | JEP Verb | Semantics |
|-----------------------|----------|-----------|
| AI ranks/screen candidate | J | `what` = hash of ranking output + job description |
| HR reviews AI recommendation | D | Delegation to human recruiter |
| HR makes final hire/reject decision | T | Termination with final status |
| Discrimination audit | V | Verify J→D→T chain + bias metrics |

---

## Extension Schema

```json
{
  "extensions": {
    "https://jep-eu-compliance.org/industry/hr": {
      "job_id_hash": "sha256:job-description-hash",
      "candidate_anon_id": "sha256:salted-candidate-id",
      "bias_audit_flag": false,
      "diversity_metric_hash": "sha256:diversity-report-hash",
      "human_final_decision": true,
      "human_recruiter_did": "did:example:tmp:recruiter-321",
      "decision_outcome": "rejected",
      "explanation_provided": true,
      "candidate_notification_hash": "sha256:notification-hash"
    }
  }
}
```

### Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `job_id_hash` | string | Hash of job description/requisition | Yes |
| `candidate_anon_id` | string | Salted hash — no plaintext PII | Yes |
| `bias_audit_flag` | boolean | True if bias detected in audit | No |
| `diversity_metric_hash` | string | Hash of diversity/equity report | Yes |
| `human_final_decision` | boolean | Must be true for Annex III compliance | Yes |
| `human_recruiter_did` | string | DID of decision-making recruiter | Yes |
| `decision_outcome` | string | `hired`, `rejected`, `interview`, `on_hold` | Yes |
| `explanation_provided` | boolean | GDPR Art. 22 + transparency requirement | Yes |
| `candidate_notification_hash` | string | Hash of notification sent to candidate | Yes |

---

## Verification Strategy

1. **Signature & nonce** (JEP core)
2. **PII protection**: `candidate_anon_id` MUST be salted hash; plaintext PII = INVALID
3. **Human decision gate**: `human_final_decision: true` requires T event signed by `human_recruiter_did`
4. **Bias audit**: If `bias_audit_flag: true`, chain MUST contain subsequent V event documenting mitigation
5. **Notification trace**: `candidate_notification_hash` proves transparency obligation met
6. **Retention**: 6 months minimum; discrimination claim periods per national law may extend

---

## Compliance Output Example

**Scenario**: AI screens 200 resumes → Shortlists 10 → HR interviews → Final rejection with explanation

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:hr-ai-agent",
  "when": 1742345678,
  "what": "sha256:shortlist-output-hash",
  "nonce": "uuid-301",
  "aud": "https://corp.example.com",
  "ref": null,
  "sig": "...",
  "extensions": {
    "https://jep-eu-compliance.org/industry/hr": {
      "job_id_hash": "sha256:job-123-hash",
      "candidate_anon_id": "sha256:salted-id-abc",
      "diversity_metric_hash": "sha256:diversity-hash",
      "human_final_decision": true,
      "decision_outcome": "rejected",
      "explanation_provided": true,
      "candidate_notification_hash": "sha256:notify-hash"
    }
  }
}
```

```json
{
  "jep": "1",
  "verb": "T",
  "who": "did:example:tmp:recruiter-321",
  "when": 1742345900,
  "what": "sha256:final-decision-hash",
  "nonce": "uuid-302",
  "aud": "https://corp.example.com",
  "ref": "sha256:shortlist-output-hash",
  "sig": "...",
  "extensions": {
    "https://jep-eu-compliance.org/industry/hr": {
      "human_recruiter_did": "did:example:tmp:recruiter-321",
      "decision_outcome": "rejected",
      "override_reason": "Selected candidate with stronger domain expertise"
    }
  }
}