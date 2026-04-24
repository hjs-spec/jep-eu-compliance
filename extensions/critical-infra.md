# Critical Infrastructure Extension

**EU AI Act Reference**: Annex III (2) — Management & operation of critical infrastructure (energy, water, transport, digital infrastructure)  
**Risk Class**: High-risk  
**JEP Industry Identifier**: `https://jep-eu-compliance.org/industry/critical-infra`

---

## Regulatory Context

AI systems managing energy grids, water supply, transport networks, or digital infrastructure are high-risk under Annex III (2). Failure or malfunction may cause physical damage or harm to persons.

Key obligations:
- Risk management with safety lifecycle (Art. 9)
- Human oversight with intervention & override (Art. 14)
- Accuracy, robustness, cybersecurity (Art. 15)
- Automatic logging (Art. 12)
- Post-market monitoring for safety incidents (Art. 72)

---

## JEP Primitive Mapping

| EU AI Act Requirement | JEP Verb | Semantics |
|-----------------------|----------|-----------|
| AI initiates control command | J | `what` = hash of command + system state |
| Operator assumes control | D | Delegation to human operator |
| Emergency shutdown / safe mode | T | Termination with `safe_state` flag |
| Incident investigation | V | Verify causal chain + system state |

---

## Extension Schema

```json
{
  "extensions": {
    "https://jep-eu-compliance.org/industry/critical-infra": {
      "infra_type": "energy_grid",
      "system_state_hash": "sha256:scada-state-hash",
      "command_type": "load_balancing",
      "operator_did": "did:example:tmp:operator-001",
      "cybersecurity_threat_level": "low",
      "physical_safety_impact": "none",
      "redundancy_activated": false,
      "safe_state_available": true,
      "nist_csf_alignment": "PR.IP-1"
    }
  }
}
```

### Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `infra_type` | string | `energy_grid`, `water_supply`, `transport`, `digital_infra` | Yes |
| `system_state_hash` | string | Hash of SCADA/OT system state snapshot | Yes |
| `command_type` | string | Classification of AI command | Yes |
| `operator_did` | string | DID of supervising human operator | Yes |
| `cybersecurity_threat_level` | string | `none`, `low`, `medium`, `high`, `critical` | Yes |
| `physical_safety_impact` | string | `none`, `minor`, `major`, `catastrophic` | Yes |
| `redundancy_activated` | boolean | True if fallback system engaged | No |
| `safe_state_available` | boolean | True if safe-state transition possible | Yes |
| `nist_csf_alignment` | string | NIST CSF or equivalent framework reference | No |

---

## Verification Strategy

1. **Signature & nonce** (JEP core)
2. **Operator presence**: High-risk command MUST have `operator_did` with valid D or T in chain
3. **Safety check**: If `physical_safety_impact` ≥ `major`, chain MUST demonstrate human approval (D) before execution
4. **Cybersecurity**: `cybersecurity_threat_level` ≥ `high` MUST trigger additional V event
5. **Safe state**: T event MUST verify `safe_state_available` was true at termination
6. **Retention**: 6 months minimum + sector-specific safety regulations

---

## Compliance Output Example

**Scenario**: AI detects grid imbalance → Recommends load shift → Operator approves

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:grid-ai-agent",
  "when": 1742345678,
  "what": "sha256:load-shift-command-hash",
  "nonce": "uuid-501",
  "aud": "https://grid.example.com",
  "ref": null,
  "sig": "...",
  "extensions": {
    "https://jep-eu-compliance.org/industry/critical-infra": {
      "infra_type": "energy_grid",
      "system_state_hash": "sha256:scada-hash",
      "command_type": "load_balancing",
      "operator_did": "did:example:tmp:operator-001",
      "cybersecurity_threat_level": "low",
      "physical_safety_impact": "none",
      "safe_state_available": true
    }
  }
}
```

```json
{
  "jep": "1",
  "verb": "D",
  "who": "did:example:tmp:operator-001",
  "when": 1742345685,
  "what": "sha256:approval-hash",
  "nonce": "uuid-502",
  "aud": "https://grid.example.com",
  "ref": "sha256:load-shift-command-hash",
  "sig": "...",
  "extensions": {
    "https://jep-eu-compliance.org/industry/critical-infra": {
      "operator_did": "did:example:tmp:operator-001",
      "approval_method": "mfa_console",
      "override_capability": true
    }
  }
}