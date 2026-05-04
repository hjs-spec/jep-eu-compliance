> **Exploratory mapping note. Not legal advice. Not part of JEP-Core.**
>
> This file describes possible JEP extension/profile fields for discussion only.

# Autonomous Driving & Traffic Safety Extension

**EU AI Act Reference**: Annex III (2) — Management & operation of critical infrastructure (traffic safety)  
**Risk Class**: High-risk  
**JEP Industry Identifier**: `https://jep-eu-compliance mapping.org/industry/automotive`

---

## Regulatory Context

AI systems managing traffic safety or embedded in vehicles as safety components are high-risk under Annex III (2). From August 2027, Annex I (vehicle type-approval frameworks) also applies.

Key obligations:
- Risk management covering safety lifecycle (Art. 9)
- Human oversight with safe-state transition (Art. 14)
- Automatic logging with sensor fusion traceability (Art. 12)
- Accuracy & robustness against adversarial inputs (Art. 15)
- Post-market monitoring for safety incidents (Art. 72)

---

## JEP Primitive Mapping

| EU AI Act Requirement | JEP Verb | Semantics |
|-----------------------|----------|-----------|
| AI initiates driving decision | J | `what` = hash of sensor fusion + decision frame |
| Safety driver takes over | D | Delegation to human operator |
| Emergency stop / safe state | T | Termination with `safety_state` flag |
| Accident reconstruction | V | Verify "who was driving" timeline |

---

## Extension Schema

```json
{
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/automotive": {
      "vehicle_vin": "sha256:hashed-vin",
      "sensor_fusion_hash": "sha256:lidar-radar-camera-fusion",
      "decision_frame_id": "frame-1742345678-001",
      "odometer_km": 45231.7,
      "geo_hash": "u4pruydqqvj",
      "safety_driver_present": true,
      "safety_driver_did": "did:example:tmp:driver-001",
      "operational_domain": "urban_l4",
      "adversarial_test_passed": true,
      "safe_state_triggered": false
    }
  }
}
```

### Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `vehicle_vin` | string | Salted hash of Vehicle Identification Number | Yes |
| `sensor_fusion_hash` | string | Hash of fused sensor data at decision moment | Yes |
| `decision_frame_id` | string | Unique frame identifier | Yes |
| `odometer_km` | number | Odometer reading | Yes |
| `geo_hash` | string | Geohash of location (precision per privacy policy) | Yes |
| `safety_driver_present` | boolean | True if human monitor in vehicle | Yes |
| `safety_driver_did` | string | DID of safety driver | If present |
| `operational_domain` | string | `highway_l3`, `urban_l4`, `parking_l5`, etc. | Yes |
| `adversarial_test_passed` | boolean | Model passed latest adversarial robustness test | Yes |
| `safe_state_triggered` | boolean | True if T event triggered safe-state | No |

---

## Verification Strategy

1. **Signature & nonce** (JEP core)
2. **Temporal integrity**: Frame IDs must be monotonic within trip
3. **Sensor traceability**: `sensor_fusion_hash` must match raw sensor logs
4. **Human takeover evidence**: If `safe_state_triggered: true`, chain MUST contain preceding D or T within 5 seconds
5. **Location privacy**: `geo_hash` precision MUST comply with local data protection law
6. **Retention**: 6 months minimum; accident-related chains retained per national traffic law

---

## Compliance Mapping Output Example

**Scenario**: L4 urban driving → Pedestrian detected → AI brakes → Safety driver confirms

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:tmp:autopilot-agent",
  "when": 1742345678,
  "what": "sha256:brake-decision-hash",
  "nonce": "uuid-201",
  "aud": "https://fleet.example.com",
  "ref": null,
  "sig": "...",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/automotive": {
      "vehicle_vin": "sha256:vin-hash",
      "sensor_fusion_hash": "sha256:sensor-hash",
      "decision_frame_id": "frame-1742345678-001",
      "odometer_km": 45231.7,
      "geo_hash": "u4pruydqqvj",
      "safety_driver_present": true,
      "safety_driver_did": "did:example:tmp:driver-001",
      "operational_domain": "urban_l4",
      "adversarial_test_passed": true
    }
  }
}
```

```json
{
  "jep": "1",
  "verb": "T",
  "who": "did:example:tmp:driver-001",
  "when": 1742345681,
  "what": "sha256:human-confirm-hash",
  "nonce": "uuid-202",
  "aud": "https://fleet.example.com",
  "ref": "sha256:brake-decision-hash",
  "sig": "...",
  "ext": {
    "https://jep-eu-compliance mapping.org/industry/automotive": {
      "safe_state_triggered": false,
      "override_reason": null,
      "final_control": "ai_maintained"
    }
  }
}