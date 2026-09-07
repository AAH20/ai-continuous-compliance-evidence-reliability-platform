"""Fail-closed evidence qualification."""

from datetime import timedelta
from typing import Any

from .canonical import receipt_sha256
from .models import GateStatus, parse_time


def qualify_evidence(record: dict[str, Any], *, as_of: str, max_age_hours: int = 24) -> dict:
    if max_age_hours <= 0:
        raise ValueError("max_age_hours must be positive")
    evaluation = parse_time(as_of)
    collected = parse_time(record.get("collected_at", ""))
    valid_from = parse_time(record.get("valid_from", ""))
    valid_until = parse_time(record.get("valid_until", ""))
    audit_start = parse_time(record.get("audit_period_start", ""))
    audit_end = parse_time(record.get("audit_period_end", ""))
    expected, observed = set(record.get("expected_scope", [])), set(record.get("observed_scope", []))
    target_controls = set(record.get("target_control_ids", []))
    control_ids = set(record.get("control_ids", []))
    supplied_digest = record.get("payload_sha256")
    calculated_digest = receipt_sha256(record.get("payload"))

    checks = [
        ("provenance", bool(record.get("source") and record.get("resource") and record.get("collector")), "source, resource and collector are identified"),
        ("integrity", bool(supplied_digest and supplied_digest == calculated_digest), "payload digest matches the retained receipt"),
        ("scope", bool(expected and expected <= observed), "all expected resources are observed"),
        ("freshness", collected <= evaluation <= collected + timedelta(hours=max_age_hours), "artifact is current at evaluation time"),
        ("relevance", bool(target_controls and target_controls <= control_ids), "artifact supports every evaluated control"),
        ("temporal_validity", valid_from <= collected <= valid_until and audit_start <= collected <= audit_end and valid_from <= evaluation <= valid_until, "collection and evaluation fall inside validity and audit windows"),
    ]
    gates = [{"gate": name, "status": GateStatus.PASS.value if passed else GateStatus.FAIL.value, "reason": reason} for name, passed, reason in checks]
    result = {"artifact_id": record.get("artifact_id"), "qualified": all(passed for _, passed, _ in checks), "gates": gates, "calculated_payload_sha256": calculated_digest}
    result["receipt_sha256"] = receipt_sha256(result)
    return result
