#!/usr/bin/env python3
"""
Unit tests for JEP EU Compliance Verifier.

Usage: python -m pytest test_verify_jep_eu.py -v
License: MIT
"""

import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from verify_jep_eu import verify_jep_core, verify_extension, detect_industry


class TestCoreVerification:
    """Test JEP core structure validation."""

    def test_valid_core(self):
        event = {
            "jep": "1",
            "verb": "J",
            "who": "did:example:tmp:agent-123",
            "when": 1742345678,
            "what": "sha256:abc123",
            "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "sig": "test-sig",
            "ref": None
        }
        ok, errs = verify_jep_core(event)
        assert ok and len(errs) == 0

    def test_missing_jep_version(self):
        event = {
            "verb": "J",
            "who": "did:example:tmp:agent-123",
            "when": 1742345678,
            "what": "sha256:abc123",
            "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "sig": "test-sig"
        }
        ok, errs = verify_jep_core(event)
        assert not ok
        assert any("MISSING_CORE_FIELD" in e for e in errs)

    def test_invalid_verb(self):
        event = {
            "jep": "1",
            "verb": "X",
            "who": "did:example:tmp:agent-123",
            "when": 1742345678,
            "what": "sha256:abc123",
            "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "sig": "test-sig"
        }
        ok, errs = verify_jep_core(event)
        assert not ok
        assert any("INVALID_VERB" in e for e in errs)

    def test_root_j_with_ref(self):
        event = {
            "jep": "1",
            "verb": "J",
            "who": "did:example:tmp:agent-123",
            "when": 1742345678,
            "what": "sha256:abc123",
            "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "sig": "test-sig",
            "ref": "sha256:some-parent"
        }
        ok, errs = verify_jep_core(event)
        assert not ok
        assert any("ROOT_J_MUST_HAVE_NULL_REF" in e for e in errs)

    def test_invalid_nonce_format(self):
        event = {
            "jep": "1",
            "verb": "J",
            "who": "did:example:tmp:agent-123",
            "when": 1742345678,
            "what": "sha256:abc123",
            "nonce": "not-a-uuid",
            "sig": "test-sig"
        }
        ok, errs = verify_jep_core(event)
        assert not ok
        assert any("INVALID_NONCE_FORMAT" in e for e in errs)


class TestMedicalExtension:
    """Test medical industry extension validation."""

    def test_valid_medical(self):
        ext = {
            "diagnosis_code": "ICD-11:2A00",
            "input_data_hash": "sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
            "confidence_score": 0.94,
            "human_review_required": True,
            "human_reviewer_did": "did:example:tmp:doctor-456",
            "model_version_hash": "sha256:f29bc64a96b7964da0551f3efa61e2ce964b8741234567890abcdef1234567890",
            "mdr_class": "IIa",
            "post_market_monitoring_id": "pm-2026-001"
        }
        ok, errs = verify_extension("medical", ext)
        assert ok and len(errs) == 0

    def test_missing_human_reviewer(self):
        ext = {
            "diagnosis_code": "ICD-11:2A00",
            "input_data_hash": "sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
            "confidence_score": 0.94,
            "human_review_required": True,
            "model_version_hash": "sha256:f29bc64a96b7964da0551f3efa61e2ce964b8741234567890abcdef1234567890",
            "post_market_monitoring_id": "pm-2026-001"
        }
        ok, errs = verify_extension("medical", ext)
        assert not ok
        assert any("MISSING_CONDITIONAL" in e for e in errs)

    def test_invalid_confidence_range(self):
        ext = {
            "diagnosis_code": "ICD-11:2A00",
            "input_data_hash": "sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
            "confidence_score": 1.5,
            "human_review_required": False,
            "model_version_hash": "sha256:f29bc64a96b7964da0551f3efa61e2ce964b8741234567890abcdef1234567890",
            "post_market_monitoring_id": "pm-2026-001"
        }
        ok, errs = verify_extension("medical", ext)
        assert not ok
        assert any("OUT_OF_RANGE" in e for e in errs)

    def test_invalid_hash_format(self):
        ext = {
            "diagnosis_code": "ICD-11:2A00",
            "input_data_hash": "invalid-hash",
            "confidence_score": 0.94,
            "human_review_required": False,
            "model_version_hash": "sha256:f29bc64a96b7964da0551f3efa61e2ce964b8741234567890abcdef1234567890",
            "post_market_monitoring_id": "pm-2026-001"
        }
        ok, errs = verify_extension("medical", ext)
        assert not ok
        assert any("INVALID_HASH_FORMAT" in e for e in errs)


class TestFintechExtension:
    """Test fintech industry extension validation."""

    def test_valid_fintech(self):
        ext = {
            "decision_type": "credit_scoring",
            "model_version_hash": "sha256:model-v2-1-manifest-hash-1234567890abcdef",
            "feature_importance_hash": "sha256:shap-values-hash-fedcba0987654321",
            "adverse_action_notice": True,
            "gdpr_art22_compliant": True,
            "applicant_consent_hash": "sha256:consent-record-hash-abcdef1234567890",
            "bias_audit_flag": False,
            "human_loan_officer_did": "did:example:tmp:officer-789",
            "explanation_hash": "sha256:explanation-text-hash-1234567890abcdef"
        }
        ok, errs = verify_extension("fintech", ext)
        assert ok and len(errs) == 0

    def test_missing_officer_on_adverse(self):
        ext = {
            "decision_type": "credit_scoring",
            "model_version_hash": "sha256:model-v2-1-manifest-hash-1234567890abcdef",
            "feature_importance_hash": "sha256:shap-values-hash-fedcba0987654321",
            "adverse_action_notice": True,
            "gdpr_art22_compliant": True,
            "applicant_consent_hash": "sha256:consent-record-hash-abcdef1234567890",
            "explanation_hash": "sha256:explanation-text-hash-1234567890abcdef"
        }
        ok, errs = verify_extension("fintech", ext)
        assert not ok
        assert any("MISSING_CONDITIONAL" in e for e in errs)

    def test_invalid_decision_type(self):
        ext = {
            "decision_type": "invalid_type",
            "model_version_hash": "sha256:model-v2-1-manifest-hash-1234567890abcdef",
            "feature_importance_hash": "sha256:shap-values-hash-fedcba0987654321",
            "adverse_action_notice": False,
            "gdpr_art22_compliant": True,
            "applicant_consent_hash": "sha256:consent-record-hash-abcdef1234567890",
            "explanation_hash": "sha256:explanation-text-hash-1234567890abcdef"
        }
        ok, errs = verify_extension("fintech", ext)
        assert not ok
        assert any("INVALID_ENUM" in e for e in errs)


class TestAutoDetection:
    """Test industry auto-detection from event extensions."""

    def test_detect_medical(self):
        event = {
            "extensions": {
                "https://jep-eu-compliance.org/industry/medical": {"test": 1}
            }
        }
        assert detect_industry(event) == "medical"

    def test_detect_fintech(self):
        event = {
            "extensions": {
                "https://jep-eu-compliance.org/industry/fintech": {"test": 1}
            }
        }
        assert detect_industry(event) == "fintech"

    def test_detect_none(self):
        event = {"extensions": {}}
        assert detect_industry(event) is None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])