"""
Risk and Fraud Agent: Forensic telemetry, discrepancy, and tamper detection engine.
Enforces physical plausibility, temporal coherence, and evidentiary authenticity.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
import hashlib


@dataclass
class DiscrepancyFlag:
    code: str
    severity: str
    finding: str
    statutory_exposure: str
    remediation_owner: str
    action_required: str


class RiskAndFraudAgent:
    """
    Forensic engine evaluating physical impossibility, synthetic entry,
    and temporal manipulation across docket data tiers.
    """

    def __init__(self, min_variance_epsilon: float = 0.0001, max_temporal_lag_hours: float = 24.0):
        self.min_variance_epsilon = min_variance_epsilon
        self.max_temporal_lag_hours = max_temporal_lag_hours

    def verify_sha256(self, raw_bytes: bytes, declared_hash: str) -> bool:
        """Enforces FRE 902(14) self-authenticating cryptographic validation."""
        computed = hashlib.sha256(raw_bytes).hexdigest()
        return computed.lower() == declared_hash.lower()

    def check_synthetic_variance(self, values: List[float]) -> bool:
        """
        Flags flat-line or artificially generated numbers.
        Physical hardware sensors calibrated to NIST standards always exhibit natural noise.
        """
        if len(values) < 2:
            return False
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance < self.min_variance_epsilon

    def evaluate_dossier_integrity(
        self,
        reported_incident_iso: str,
        calculated_t0_iso: str,
        telemetry_observations: List[float],
        signatory_metadata: Dict[str, Any],
        raw_evidence_bytes: bytes = None,
        manifest_hash: str = None
    ) -> Dict[str, Any]:
        """
        Runs forensic integrity checks across the docket payload.
        Returns circuit breaker state and structured discrepancy findings.
        """
        flags: List[DiscrepancyFlag] = []

        # 1. Temporal Drift Inconsistency
        t_incident = datetime.fromisoformat(reported_incident_iso.replace("Z", "+00:00"))
        t_onset = datetime.fromisoformat(calculated_t0_iso.replace("Z", "+00:00"))
        lag_hours = (t_incident - t_onset).total_seconds() / 3600.0

        if lag_hours > self.max_temporal_lag_hours:
            flags.append(DiscrepancyFlag(
                code="ERR_TEMPORAL_MISMATCH",
                severity="CRITICAL",
                finding=f"Incident claimed as sudden at {reported_incident_iso}, but physical drift (t₀) initiated {lag_hours:.1f} hours prior at {calculated_t0_iso}.",
                statutory_exposure="Misrepresentation of operational baseline; loss of Business Judgment protection.",
                remediation_owner="Chief Operating Officer",
                action_required="Audit prior shift handovers; void sudden-onset narrative."
            ))

        # 2. Synthetic Data / Missing Physical Variance
        if self.check_synthetic_variance(telemetry_observations):
            flags.append(DiscrepancyFlag(
                code="ERR_SYNTHETIC_TELEMETRY",
                severity="CRITICAL",
                finding="Observation series exhibits zero physical noise variance. Indicates manufactured or manually smoothed values.",
                statutory_exposure="Spoliation of evidence; inadmissible under FRE 902(14).",
                remediation_owner="Senior Systems Safety Engineer (PE)",
                action_required="Subpoena raw binary stream directly from NIST-calibrated IMU/DSSAD logger."
            ))

        # 3. Cryptographic Tamper Check
        if raw_evidence_bytes and manifest_hash:
            if not self.verify_sha256(raw_evidence_bytes, manifest_hash):
                flags.append(DiscrepancyFlag(
                    code="ERR_EVID_HASH_MISMATCH",
                    severity="CRITICAL",
                    finding="Dataset SHA-256 does not match ingestion manifest. Evidence altered post-collection.",
                    statutory_exposure="Potential criminal spoliation and civil fraud liability.",
                    remediation_owner="General Counsel / Independent Assessor",
                    action_required="Quarantine corrupted dataset; initiate independent forensic audit."
                ))

        # 4. Signatory Credential Authorization
        if not signatory_metadata.get("is_verified_pe", False):
            flags.append(DiscrepancyFlag(
                code="ERR_UNAUTHORIZED_SIGNATORY",
                severity="HIGH",
                finding="Statutory witness oath executed without an active, validated Professional Engineer license.",
                statutory_exposure="Perjury exposure under statutory declaration statutes.",
                remediation_owner="Operations Verification Desk",
                action_required="Re-assign attestation to an unconflicted, licensed Professional Engineer."
            ))

        circuit_breaker_active = len(flags) > 0

        return {
            "circuit_breaker_active": circuit_breaker_active,
            "flag_count": len(flags),
            "discrepancies": [f.__dict__ for f in flags],
            "evaluation_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
