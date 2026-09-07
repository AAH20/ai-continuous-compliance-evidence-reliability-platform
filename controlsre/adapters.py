"""Credential-free normalization contracts for supported source shapes."""

from typing import Any


def normalize_inventory(provider: str, records: list[dict[str, Any]]) -> list[str]:
    extractors = {
        "aws-organizations": lambda item: item.get("Id"),
        "kubernetes": lambda item: item.get("metadata", {}).get("uid"),
        "workflow": lambda item: item.get("source_id"),
    }
    if provider not in extractors:
        raise ValueError(f"unsupported inventory provider: {provider}")
    identifiers = [extractors[provider](record) for record in records]
    if any(not identifier for identifier in identifiers):
        raise ValueError("every inventory record must resolve to a stable identifier")
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("inventory identifiers must be unique")
    return sorted(identifiers)


def import_framework_catalog(payload: dict[str, Any]) -> dict:
    frameworks = payload.get("frameworks")
    if not isinstance(frameworks, list):
        raise ValueError("frameworks must be a list")
    urns = [item.get("urn") for item in frameworks]
    if any(not urn for urn in urns) or len(set(urns)) != len(urns):
        raise ValueError("framework URNs must be present and unique")
    return {"framework_count": len(frameworks), "framework_urns": sorted(urns), "integration_contract": "ciso-assistant-compatible"}
