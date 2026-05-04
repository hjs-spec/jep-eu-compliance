"""Exploratory mapping verifier. Not legal advice. Not a JEP-Core conformance verifier."""

#!/usr/bin/env python3
"""
JEP EU Compliance Verifier
Minimal reference implementation for validating JEP events against EU AI Act industry extensions.

Usage:
    python verify_jep_eu.py --event event.json --industry medical
    python verify_jep_eu.py --event event.json --auto-detect

Dependencies: None (stdlib only)
License: MIT
"""

import argparse
import json
import sys
import re
from pathlib import Path

# Industry-specific required fields registry
INDUSTRY_RULES = {
    "medical": {
        "required": [
            "diagnosis_code",
            "input_data_hash",
            "confidence_score",
            "human_review_required",
            "model_version_hash",
            "post_market_monitoring_id",
        ],
        "conditional": {
            "human_review_required": {
                "if_true": ["human_reviewer_did"]
            }
        },
        "hash_fields": ["input_data_hash", "model_version_hash"],
        "range_fields": {"confidence_score": (0.0, 1.0)},
    },
    "fintech": {
        "required": [
            "decision_type",
            "model_version_hash",
            "feature_importance_hash",
            "adverse_action_notice",
            "gdpr_art22_compliant",
            "applicant_consent_hash",
            "explanation_hash",
        ],
        "conditional": {
            "adverse_action_notice": {
                "if_true": ["human_loan_officer_did"]
            }
        },
        "hash_fields": [
            "model_version_hash",
            "feature_importance_hash",
            "applicant_consent_hash",
            "explanation_hash",
        ],
        "enum_fields": {
            "decision_type": ["credit_scoring", "creditworthiness", "insurance_risk", "fraud_detection"]
        },
    },
    "automotive": {
        "required": [
            "vehicle_vin",
            "sensor_fusion_hash",
            "decision_frame_id",
            "odometer_km",
            "geo_hash",
            "safety_driver_present",
            "operational_domain",
            "adversarial_test_passed",
        ],
        "conditional": {
            "safety_driver_present": {
                "if_true": ["safety_driver_did"]
            }
        },
        "hash_fields": ["vehicle_vin", "sensor_fusion_hash"],
    },
    "hr": {
        "required": [
            "job_id_hash",
            "candidate_anon_id",
            "diversity_metric_hash",
            "human_final_decision",
            "human_recruiter_did",
            "decision_outcome",
            "explanation_provided",
            "candidate_notification_hash",
        ],
        "enum_fields": {
            "decision_outcome": ["hired", "rejected", "interview", "on_hold"]
        },
        "hash_fields": [
            "job_id_hash",
            "candidate_anon_id",
            "diversity_metric_hash",
            "candidate_notification_hash",
        ],
    },
    "governance": {
        "required": [
            "disclosure_flag",
            "ai_interaction_notice_hash",
            "citizen_request_hash",
            "synthetic_content_label",
            "deepfake_flag",
            "citizen_consent_hash",
            "data_retention_policy",
            "ttl_expiry",
        ],
        "conditional": {
            "synthetic_content_label": {
                "if_true": ["machine_readable_mark"]
            }
        },
        "enum_fields": {
            "data_retention_policy": ["gdpr_minimal", "ai_act_6m", "national_archive"]
        },
        "hash_fields": [
            "ai_interaction_notice_hash",
            "citizen_request_hash",
            "citizen_consent_hash",
        ],
    },
    "critical-infra": {
        "required": [
            "infra_type",
            "system_state_hash",
            "command_type",
            "operator_did",
            "cybersecurity_threat_level",
            "physical_safety_impact",
            "safe_state_available",
        ],
        "enum_fields": {
            "infra_type": ["energy_grid", "water_supply", "transport", "digital_infra"],
            "cybersecurity_threat_level": ["none", "low", "medium", "high", "critical"],
            "physical_safety_impact": ["none", "minor", "major", "catastrophic"],
        },
        "hash_fields": ["system_state_hash"],
    },
}


def verify_jep_core(event: dict) -> tuple[bool, list[str]]:
    """Verify JEP core structure (minimal, no crypto)."""
    errors = []
    required_top = ["jep", "verb", "who", "when", "what", "nonce", "sig"]

    for field in required_top:
        if field not in event:
            errors.append(f"MISSING_CORE_FIELD: {field}")

    if event.get("jep") != "1":
        errors.append("INVALID_JEP_VERSION")

    verb = event.get("verb")
    if verb not in {"J", "D", "T", "V"}:
        errors.append(f"INVALID_VERB: {verb}")

    if not isinstance(event.get("when"), int):
        errors.append("INVALID_WHEN_TYPE")

    if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", str(event.get("nonce", "")), re.I):
        errors.append("INVALID_NONCE_FORMAT")

    # Chain integrity: root J must have ref == null or absent
    if verb == "J" and event.get("ref") is not None:
        errors.append("ROOT_J_MUST_HAVE_NULL_REF")

    return len(errors) == 0, errors


def verify_extension(industry: str, ext: dict) -> tuple[bool, list[str]]:
    """Verify industry extension fields."""
    rules = INDUSTRY_RULES.get(industry)
    if not rules:
        return False, [f"UNKNOWN_INDUSTRY: {industry}"]

    errors = []

    # Required fields
    for field in rules.get("required", []):
        if field not in ext:
            errors.append(f"MISSING_REQUIRED: {field}")

    # Conditional fields
    for trigger_field, condition in rules.get("conditional", {}).items():
        if ext.get(trigger_field) is True:
            for required in condition.get("if_true", []):
                if required not in ext:
                    errors.append(f"MISSING_CONDITIONAL: {required} (because {trigger_field}=true)")

    # Hash format validation (sha256: or sm3: prefix + hex)
    hash_pattern = re.compile(r"^(sha256|sm3):[a-fA-F0-9]+$")
    for field in rules.get("hash_fields", []):
        val = ext.get(field)
        if val is not None and not hash_pattern.match(str(val)):
            errors.append(f"INVALID_HASH_FORMAT: {field}")

    # Range validation
    for field, (lo, hi) in rules.get("range_fields", {}).items():
        val = ext.get(field)
        if val is not None and not (lo <= float(val) <= hi):
            errors.append(f"OUT_OF_RANGE: {field} ({val} not in [{lo}, {hi}])")

    # Enum validation
    for field, allowed in rules.get("enum_fields", {}).items():
        val = ext.get(field)
        if val is not None and val not in allowed:
            errors.append(f"INVALID_ENUM: {field}={val} (allowed: {allowed})")

    return len(errors) == 0, errors


def detect_industry(event: dict) -> str | None:
    """Auto-detect industry from extension keys."""
    exts = event.get("ext", event.get("extensions", {}))
    for key in exts:
        if key.startswith("https://jep-eu-compliance.org/industry/"):
            return key.split("/")[-1]
    return None


def main():
    parser = argparse.ArgumentParser(description="JEP EU Compliance Verifier")
    parser.add_argument("--event", required=True, help="Path to JEP event JSON file")
    parser.add_argument("--industry", help="Industry key (medical, fintech, automotive, hr, governance, critical-infra)")
    parser.add_argument("--auto-detect", action="store_true", help="Auto-detect industry from event extensions")
    args = parser.parse_args()

    path = Path(args.event)
    if not path.exists():
        print(f"ERROR: File not found: {args.event}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        event = json.load(f)

    # Core verification
    core_ok, core_errors = verify_jep_core(event)
    if not core_ok:
        for e in core_errors:
            print(f"CORE_ERROR: {e}")
        sys.exit(1)

    # Industry detection / selection
    industry = args.industry
    if args.auto_detect:
        industry = detect_industry(event)
        if industry:
            print(f"AUTO_DETECTED_INDUSTRY: {industry}")
        else:
            print("ERROR: Could not auto-detect industry. Use --industry.")
            sys.exit(1)

    if not industry:
        print("ERROR: No industry specified. Use --industry or --auto-detect.")
        sys.exit(1)

    # Extension verification
    exts = event.get("ext", event.get("extensions", {}))
    industry_key = f"https://jep-eu-compliance.org/industry/{industry}"
    industry_ext = exts.get(industry_key, {})

    ext_ok, ext_errors = verify_extension(industry, industry_ext)
    if not ext_ok:
        for e in ext_errors:
            print(f"EXT_ERROR: {e}")
        sys.exit(1)

    # Chain checks (basic)
    verb = event.get("verb")
    if verb in {"D", "T"} and not event.get("ref"):
        print("CHAIN_WARNING: D/T event missing ref (orphaned delegation/termination)")

    print("RESULT: VALID")
    sys.exit(0)


if __name__ == "__main__":
    main()