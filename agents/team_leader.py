"""
Team Leader Agent: Company Control Board Engagement Orchestrator.
Enforces the epistemological firewall, boundaries, and least-privilege dispatch.
"""

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
import json
from typing import Any, Dict, List, Optional


class EpistemicStatus(str, Enum):
    VERIFIED_FACT = "VERIFIED_FACT"
    REPORTED_KNOWLEDGE = "REPORTED_KNOWLEDGE"
    HYPOTHESIS = "HYPOTHESIS"


class EntityType(str, Enum):
    ASSET_POOL = "ASSET_POOL"
    BUSINESS_UNIT = "BUSINESS_UNIT"
    INFRASTRUCTURE_CORRIDOR = "INFRASTRUCTURE_CORRIDOR"
    CUSTOMER_SEGMENT = "CUSTOMER_SEGMENT"
    CONTRACT_CLASS = "CONTRACT_CLASS"


@dataclass(frozen=True)
class DataPoint:
    metric_name: str
    value: Any
    timestamp: datetime
    source_system: str
    owner_role: str
    epistemic_status: EpistemicStatus
    source_hash: Optional[str] = None
    notes: Optional[str] = None
    data_type: Optional[str] = None


@dataclass
class EngagementScope:
    problem_sponsor: str
    decision_to_support: str
    target_entity_type: EntityType
    target_entity_id: str
    jurisdiction: str
    permitted_sources: List[str]
    excluded_scope: List[str]
    prohibited_data_types: List[str] = field(
        default_factory=lambda: [
            "PERSONAL_HEALTH_RECORDS",
            "PERSONALLY_IDENTIFIABLE_INFORMATION",
            "LEGAL_PRIVILEGED_COMMUNICATIONS",
            "UNAUTHORIZED_CREDENTIALS",
        ]
    )
    authorized_update_roles: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class GovernanceEvent:
    timestamp: datetime
    event_type: str
    actor_role: str
    details_json: str


class TeamLeaderValidationError(Exception):
    """Raised when an intake fails foundational boundary or epistemic criteria."""


class TeamLeaderAgent:
    """Orchestrates the intake, verification boundary, and diagnostic dispatch."""

    SYSTEM_PROMPT = """
You are the Team Leader Agent for a Company Control Board engagement.

Your primary obligation is to protect the company’s source of truth: approved data,
intellectual property, metrics, models, documents, and operational knowledge.

Do not infer, invent, reconstruct, or claim ground truth during initial engagement.
Treat all incoming information as one of:
1. Verified fact, with an approved source and owner;
2. Reported operational knowledge, requiring validation; or
3. Hypothesis, requiring testing.

Before proposing a bottleneck solution:
- Map the actual workflow with authorised process owners.
- Identify work stages, hand-offs, queues, approvals, exception loops, controls,
  source systems, and decision rights.
- Establish the expected outcome, current observed outcome, and business consequence.
- Verify the evidence needed to apply the approved drift and acceleration model.
- Identify the earliest controllable point at which an intervention could change
  the projected outcome.

Use least-privilege tool access. Do not alter source data, send communications,
publish material, make financial commitments, accuse individuals of wrongdoing,
or make final decisions.

Every material conclusion must show:
- Source and evidence state;
- Data quality and limitations;
- Model and instruction version;
- Assumptions and uncertainty;
- Required human reviewer and decision owner.

Your output is a draft for human review, not an autonomous company decision.
"""

    def __init__(self, scope: EngagementScope):
        self.scope = scope
        self.evidence_ledger: List[DataPoint] = []
        self._governance_log: List[GovernanceEvent] = []
        self._validate_scope()
        self._record_governance_event(
            "ENGAGEMENT_INITIALIZED",
            "system",
            {
                "sponsor": scope.problem_sponsor,
                "decision_to_support": scope.decision_to_support,
                "target_entity": (
                    f"{scope.target_entity_type.value}:{scope.target_entity_id}"
                ),
                "jurisdiction": scope.jurisdiction,
                "permitted_sources": scope.permitted_sources,
            },
        )

    @property
    def governance_log(self) -> tuple[GovernanceEvent, ...]:
        """Returns an immutable view of the in-memory governance event log."""
        return tuple(self._governance_log)

    def _record_governance_event(
        self, event_type: str, actor_role: str, details: Dict[str, Any]
    ) -> None:
        self._governance_log.append(
            GovernanceEvent(
                timestamp=datetime.now().astimezone(),
                event_type=event_type,
                actor_role=actor_role,
                details_json=json.dumps(details, sort_keys=True, default=str),
            )
        )

    def _validate_scope(self, scope: Optional[EngagementScope] = None) -> None:
        """Enforces basic governance validity before accepting any engagement."""
        scope = scope or self.scope

        if not scope.problem_sponsor or len(scope.problem_sponsor.strip()) < 3:
            raise TeamLeaderValidationError(
                "ERR_GOV_MISSING_SPONSOR: Problem sponsor must be an explicit, named role."
            )

        if (
            not scope.decision_to_support
            or len(scope.decision_to_support.strip()) < 10
        ):
            raise TeamLeaderValidationError(
                "ERR_GOV_UNBOUNDED_DECISION: Decision required is vague or undefined."
            )

        if not scope.permitted_sources or any(
            not isinstance(source, str) or not source.strip()
            for source in scope.permitted_sources
        ):
            raise TeamLeaderValidationError(
                "ERR_GOV_NO_PERMITTED_SOURCES: Permitted source systems must be explicitly declared and non-empty."
            )

        if not scope.target_entity_id or not scope.target_entity_id.strip():
            raise TeamLeaderValidationError(
                "ERR_GOV_MISSING_ENTITY: A target entity ID must be provided."
            )

        if not scope.jurisdiction or not scope.jurisdiction.strip():
            raise TeamLeaderValidationError(
                "ERR_GOV_MISSING_JURISDICTION: A jurisdiction must be provided."
            )

        if any(
            not isinstance(role, str) or not role.strip()
            for role in scope.authorized_update_roles
        ):
            raise TeamLeaderValidationError(
                "ERR_GOV_INVALID_UPDATE_ROLE: Authorized update roles cannot be blank."
            )

        for field_name in (
            "permitted_sources",
            "excluded_scope",
            "prohibited_data_types",
            "authorized_update_roles",
        ):
            values = getattr(scope, field_name)
            if not isinstance(values, list) or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                raise TeamLeaderValidationError(
                    f"ERR_GOV_INVALID_SCOPE_LIST: '{field_name}' must be a list of non-empty strings."
                )

    def update_scope(self, *, actor_role: str, **changes: Any) -> None:
        """Applies an authorized, validated scope update and records it for review."""
        allowed_fields = {
            "decision_to_support",
            "target_entity_id",
            "jurisdiction",
            "permitted_sources",
            "excluded_scope",
            "prohibited_data_types",
        }
        if not actor_role or actor_role not in self.scope.authorized_update_roles:
            self._record_governance_event(
                "SCOPE_UPDATE_REJECTED",
                actor_role or "unknown",
                {"reason": "unauthorized_role", "fields": sorted(changes)},
            )
            raise TeamLeaderValidationError(
                f"ERR_GOV_UNAUTHORIZED_UPDATE: Role '{actor_role}' is not authorized to update this scope."
            )

        unsupported_fields = set(changes) - allowed_fields
        if not changes or unsupported_fields:
            self._record_governance_event(
                "SCOPE_UPDATE_REJECTED",
                actor_role,
                {
                    "reason": "empty_or_unsupported_fields",
                    "fields": sorted(changes),
                    "unsupported_fields": sorted(unsupported_fields),
                },
            )
            raise TeamLeaderValidationError(
                "ERR_GOV_INVALID_UPDATE: Supply supported scope fields only; "
                f"unsupported fields: {sorted(unsupported_fields)}."
            )

        try:
            normalized_changes = {
                field_name: list(value)
                if field_name
                in {"permitted_sources", "excluded_scope", "prohibited_data_types"}
                and isinstance(value, list)
                else value
                for field_name, value in changes.items()
            }
            updated_scope = replace(self.scope, **normalized_changes)
            self._validate_scope(updated_scope)
        except (TypeError, TeamLeaderValidationError) as error:
            self._record_governance_event(
                "SCOPE_UPDATE_REJECTED",
                actor_role,
                {
                    "reason": str(error),
                    "fields": sorted(changes),
                },
            )
            raise

        previous_values = {
            field_name: getattr(self.scope, field_name) for field_name in changes
        }
        self.scope = updated_scope
        self._record_governance_event(
            "SCOPE_UPDATED",
            actor_role,
            {
                "before": previous_values,
                "after": changes,
            },
        )

    def ingest_data_point(self, point: DataPoint) -> None:
        """Registers incoming data only if it meets source and evidence boundaries."""
        if point.source_system not in self.scope.permitted_sources:
            self._record_governance_event(
                "DATA_INGESTION_REJECTED",
                point.owner_role,
                {
                    "metric": point.metric_name,
                    "source_system": point.source_system,
                    "reason": "source_not_permitted",
                },
            )
            raise TeamLeaderValidationError(
                f"ERR_SCOPE_VIOLATION: Source system '{point.source_system}' "
                f"is not in permitted sources list: {self.scope.permitted_sources}"
            )

        if point.data_type in self.scope.prohibited_data_types:
            self._record_governance_event(
                "DATA_INGESTION_REJECTED",
                point.owner_role,
                {
                    "metric": point.metric_name,
                    "source_system": point.source_system,
                    "data_type": point.data_type,
                    "reason": "prohibited_data_type",
                },
            )
            raise TeamLeaderValidationError(
                f"ERR_GOV_PROHIBITED_DATA: Data type '{point.data_type}' is prohibited."
            )

        if point.epistemic_status == EpistemicStatus.VERIFIED_FACT:
            if not point.source_hash or not point.timestamp:
                self._record_governance_event(
                    "DATA_INGESTION_REJECTED",
                    point.owner_role,
                    {
                        "metric": point.metric_name,
                        "source_system": point.source_system,
                        "reason": "verified_fact_missing_hash_or_timestamp",
                    },
                )
                raise TeamLeaderValidationError(
                    f"ERR_EVID_UNAUTHENTICATED: Metric '{point.metric_name}' "
                    "claimed as VERIFIED_FACT but lacks SHA-256 hash or timestamp."
                )

        self.evidence_ledger.append(point)
        self._record_governance_event(
            "DATA_INGESTED",
            point.owner_role,
            {
                "metric": point.metric_name,
                "source_system": point.source_system,
                "epistemic_status": point.epistemic_status.value,
                "timestamp": point.timestamp,
                "source_hash": point.source_hash,
                "data_type": point.data_type,
            },
        )

    def extract_mathematical_baseline(self) -> Dict[str, Any]:
        """Extracts verified observations for the Kinetic Drift Engine."""
        verified_points = [
            point
            for point in self.evidence_ledger
            if point.epistemic_status == EpistemicStatus.VERIFIED_FACT
        ]

        if len(verified_points) < 3:
            raise TeamLeaderValidationError(
                "ERR_MATH_INSUFFICIENT_GROUND_TRUTH: Minimum 3 verified historical "
                f"observations required. Found: {len(verified_points)}"
            )

        return {
            "entity": (
                f"{self.scope.target_entity_type.value}:{self.scope.target_entity_id}"
            ),
            "jurisdiction": self.scope.jurisdiction,
            "observations": [
                {
                    "timestamp": point.timestamp.isoformat(),
                    "metric": point.metric_name,
                    "value": point.value,
                    "hash": point.source_hash,
                }
                for point in verified_points
            ],
        }

    def dispatch_forensic_pipeline(self) -> Dict[str, Any]:
        """Packages qualified ground truth and context for downstream analysis."""
        ground_truth_payload = self.extract_mathematical_baseline()
        now = datetime.utcnow()

        return {
            "case_id": f"CCB-{int(now.timestamp())}",
            "sponsor": self.scope.problem_sponsor,
            "decision_target": self.scope.decision_to_support,
            "ground_truth": ground_truth_payload,
            "reported_context": [
                {
                    "metric": point.metric_name,
                    "statement": point.value,
                    "owner": point.owner_role,
                }
                for point in self.evidence_ledger
                if point.epistemic_status == EpistemicStatus.REPORTED_KNOWLEDGE
            ],
            "hypotheses": [
                {"claim": point.value, "metric": point.metric_name}
                for point in self.evidence_ledger
                if point.epistemic_status == EpistemicStatus.HYPOTHESIS
            ],
            "dispatch_timestamp": now.isoformat() + "Z",
        }