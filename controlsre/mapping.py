"""Conservative framework cross-mapping semantics."""

from typing import Any

from .models import MappingRelationship


def propagate_assertion(assertion: dict[str, Any], mapping: dict[str, Any]) -> dict:
    relationship = MappingRelationship(mapping["relationship"])
    strength = mapping.get("strength", 0)
    if not isinstance(strength, (int, float)) or not 0 <= strength <= 1:
        raise ValueError("mapping strength must be between zero and one")
    if not mapping.get("rationale") or not mapping.get("source_reference"):
        raise ValueError("mapping rationale and source_reference are required")
    full = relationship in {MappingRelationship.EQUAL, MappingRelationship.SUPERSET}
    inherited = bool(assertion.get("qualified") and full)
    reason = "full relationship permits qualified inheritance" if inherited else "partial, conflicting, or unqualified relationship requires target evidence"
    return {"source_control": mapping["source_control"], "target_control": mapping["target_control"], "relationship": relationship.value, "strength": strength, "inherited_compliance": inherited, "additional_evidence_required": not inherited, "reason": reason}


def detect_mapping_conflicts(mappings: list[dict[str, Any]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], set[str]] = {}
    for mapping in mappings:
        key = (mapping["source_control"], mapping["target_control"])
        grouped.setdefault(key, set()).add(MappingRelationship(mapping["relationship"]).value)
    return [{"source_control": source, "target_control": target, "relationships": ",".join(sorted(relationships))} for (source, target), relationships in grouped.items() if len(relationships) > 1]
