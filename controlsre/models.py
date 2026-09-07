"""Shared enums and validation helpers."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any


class GateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class EvidenceLevel(str, Enum):
    VERIFIED = "VERIFIED"
    OBSERVED = "OBSERVED"
    DOCUMENTED = "DOCUMENTED"
    UNVERIFIED = "UNVERIFIED"


class MappingRelationship(str, Enum):
    EQUAL = "equal"
    SUBSET = "subset"
    SUPERSET = "superset"
    INTERSECT = "intersect"
    CONFLICTS_WITH = "conflicts_with"
    REQUIRES_ADDITIONAL_EVIDENCE = "requires_additional_evidence"


def parse_time(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO 8601 string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def require_non_negative(data: dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        value = data.get(key, 0)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{key} must be a non-negative number")
