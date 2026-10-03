"""
Tests for RiskAndFraudAgent: forensic telemetry, discrepancy, and tamper detection.
"""

import hashlib

import pytest

from agents.risk_and_fraud import DiscrepancyFlag, RiskAndFraudAgent


@pytest.fixture
def agent():
    return RiskAndFraudAgent()


def _base_signatory(verified: bool = True):
    return {"is_verified_pe": verified}


# ---------------------------------------------------------------------------
# verify_sha256
# ---------------------------------------------------------------------------

class TestVerifySha256:
    def test_matching_hash_returns_true(self, agent):
        raw = b"telemetry-payload"
        declared = hashlib.sha256(raw).hexdigest()
        assert agent.verify_sha256(raw, declared) is True

    def test_mismatched_hash_returns_false(self, agent):
        raw = b"telemetry-payload"
        assert agent.verify_sha256(raw, "0" * 64) is False

    def test_hash_comparison_is_case_insensitive(self, agent):
        raw = b"telemetry-payload"
        declared = hashlib.sha256(raw).hexdigest().upper()
        assert agent.verify_sha256(raw, declared) is True


# ---------------------------------------------------------------------------
# check_synthetic_variance
# ---------------------------------------------------------------------------

class TestCheckSyntheticVariance:
    def test_flat_line_values_flagged_as_synthetic(self, agent):
        assert agent.check_synthetic_variance([1.0, 1.0, 1.0, 1.0]) is True

    def test_naturally_noisy_values_not_flagged(self, agent):
        assert agent.check_synthetic_variance([1.0, 1.4, 0.8, 1.2, 0.95]) is False

    def test_single_value_is_not_flagged(self, agent):
        # Variance is undefined with < 2 points; method defensively returns False.
        assert agent.check_synthetic_variance([5.0]) is False

    def test_empty_list_is_not_flagged(self, agent):
        assert agent.check_synthetic_variance([]) is False

    def test_variance_at_epsilon_boundary_is_not_flagged(self, agent):
        # variance must be strictly less than epsilon to be flagged.
        custom_agent = RiskAndFraudAgent(min_variance_epsilon=0.25)
        # values [0, 1] -> mean 0.5, variance 0.25 (equal to epsilon, not < epsilon)
        assert custom_agent.check_synthetic_variance([0.0, 1.0]) is False

    def test_variance_just_below_epsilon_is_flagged(self, agent):
        custom_agent = RiskAndFraudAgent(min_variance_epsilon=0.3)
        assert custom_agent.check_synthetic_variance([0.0, 1.0]) is True


# ---------------------------------------------------------------------------
# evaluate_dossier_integrity
# ---------------------------------------------------------------------------

class TestEvaluateDossierIntegrity:
    def test_clean_dossier_raises_no_flags(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2, 0.95],
            signatory_metadata=_base_signatory(True),
        )
        assert result["circuit_breaker_active"] is False
        assert result["flag_count"] == 0
        assert result["discrepancies"] == []
        assert "evaluation_utc" in result

    def test_temporal_mismatch_flagged_beyond_threshold(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T08:00:00Z",  # 4h prior, default threshold 24h -> not flagged
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
        )
        assert result["flag_count"] == 0

        result_breach = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-02T12:00:00Z",
            calculated_t0_iso="2026-01-01T08:00:00Z",  # 28h prior -> exceeds 24h threshold
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
        )
        codes = [f["code"] for f in result_breach["discrepancies"]]
        assert "ERR_TEMPORAL_MISMATCH" in codes
        assert result_breach["circuit_breaker_active"] is True

    def test_temporal_mismatch_respects_custom_threshold(self):
        custom_agent = RiskAndFraudAgent(max_temporal_lag_hours=1.0)
        result = custom_agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T10:00:00Z",  # 2h prior -> exceeds 1h threshold
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_TEMPORAL_MISMATCH" in codes

    def test_synthetic_telemetry_flagged(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[2.0, 2.0, 2.0, 2.0],
            signatory_metadata=_base_signatory(True),
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_SYNTHETIC_TELEMETRY" in codes
        assert result["circuit_breaker_active"] is True

    def test_evidence_hash_mismatch_flagged(self, agent):
        raw_bytes = b"original-evidence"
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
            raw_evidence_bytes=raw_bytes,
            manifest_hash="deadbeef" * 8,
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_EVID_HASH_MISMATCH" in codes

    def test_evidence_hash_match_not_flagged(self, agent):
        raw_bytes = b"original-evidence"
        correct_hash = hashlib.sha256(raw_bytes).hexdigest()
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
            raw_evidence_bytes=raw_bytes,
            manifest_hash=correct_hash,
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_EVID_HASH_MISMATCH" not in codes

    def test_hash_check_skipped_when_evidence_or_manifest_missing(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
            raw_evidence_bytes=None,
            manifest_hash=None,
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_EVID_HASH_MISMATCH" not in codes

    def test_unauthorized_signatory_flagged(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(False),
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_UNAUTHORIZED_SIGNATORY" in codes

    def test_unauthorized_signatory_flagged_when_key_missing(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata={},
        )
        codes = [f["code"] for f in result["discrepancies"]]
        assert "ERR_UNAUTHORIZED_SIGNATORY" in codes

    def test_multiple_discrepancies_all_reported(self, agent):
        raw_bytes = b"original-evidence"
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-02T12:00:00Z",
            calculated_t0_iso="2026-01-01T08:00:00Z",  # temporal breach
            telemetry_observations=[2.0, 2.0, 2.0],  # synthetic
            signatory_metadata=_base_signatory(False),  # unauthorized
            raw_evidence_bytes=raw_bytes,
            manifest_hash="0" * 64,  # mismatch
        )
        codes = {f["code"] for f in result["discrepancies"]}
        assert codes == {
            "ERR_TEMPORAL_MISMATCH",
            "ERR_SYNTHETIC_TELEMETRY",
            "ERR_EVID_HASH_MISMATCH",
            "ERR_UNAUTHORIZED_SIGNATORY",
        }
        assert result["flag_count"] == 4
        assert result["circuit_breaker_active"] is True

    def test_accepts_non_utc_offset_timestamps(self, agent):
        # fromisoformat should handle explicit offsets as well as 'Z' suffix.
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00+00:00",
            calculated_t0_iso="2026-01-01T11:00:00+00:00",
            telemetry_observations=[1.0, 1.4, 0.8, 1.2],
            signatory_metadata=_base_signatory(True),
        )
        assert result["flag_count"] == 0

    def test_discrepancy_flag_dict_has_expected_fields(self, agent):
        result = agent.evaluate_dossier_integrity(
            reported_incident_iso="2026-01-01T12:00:00Z",
            calculated_t0_iso="2026-01-01T11:00:00Z",
            telemetry_observations=[1.0, 1.0],
            signatory_metadata=_base_signatory(False),
        )
        flag = result["discrepancies"][0]
        expected_keys = {
            "code",
            "severity",
            "finding",
            "statutory_exposure",
            "remediation_owner",
            "action_required",
        }
        assert expected_keys.issubset(flag.keys())


def test_discrepancy_flag_is_constructible_directly():
    flag = DiscrepancyFlag(
        code="ERR_TEST",
        severity="LOW",
        finding="Test finding",
        statutory_exposure="None",
        remediation_owner="QA",
        action_required="None",
    )
    assert flag.code == "ERR_TEST"
