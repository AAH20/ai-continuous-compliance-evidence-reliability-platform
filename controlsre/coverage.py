"""Expected-versus-observed population reconciliation."""

from typing import Iterable

from .canonical import receipt_sha256


def reconcile_population(expected: Iterable[str], observed: Iterable[str]) -> dict:
    expected_set, observed_set = set(expected), set(observed)
    if not expected_set:
        raise ValueError("expected population cannot be empty")
    if "" in expected_set | observed_set:
        raise ValueError("population identifiers cannot be empty")
    missing = sorted(expected_set - observed_set)
    unexpected = sorted(observed_set - expected_set)
    matched = sorted(expected_set & observed_set)
    result = {
        "expected_count": len(expected_set), "observed_count": len(observed_set),
        "matched_count": len(matched), "recall": round(len(matched) / len(expected_set), 6),
        "complete": not missing, "missing": missing, "unexpected": unexpected,
    }
    result["receipt_sha256"] = receipt_sha256(result)
    return result
