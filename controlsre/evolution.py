"""Turn incidents into deterministic regression cases."""

from typing import Any

from .canonical import receipt_sha256


def build_regression_case(incident: dict[str, Any]) -> dict:
    required = ["incident_id", "failure_class", "trigger", "expected_safe_behavior"]
    missing = [key for key in required if not incident.get(key)]
    if missing:
        raise ValueError(f"missing regression fields: {', '.join(missing)}")
    forbidden = {"secret", "token", "password", "customer_email"}
    leaked = sorted(forbidden & set(incident))
    if leaked:
        raise ValueError(f"sensitive fields must be removed: {', '.join(leaked)}")
    case = {"case_id": f"REG-{incident['incident_id']}", "failure_class": incident["failure_class"], "trigger": incident["trigger"], "expected_safe_behavior": incident["expected_safe_behavior"], "sanitized": True}
    case["receipt_sha256"] = receipt_sha256(case)
    return case
