"""Finance-safe unit economics and revenue-assurance boundaries."""

from typing import Any

from .canonical import receipt_sha256
from .models import require_non_negative


ECONOMIC_FIELDS = ["collector_cost", "storage_cost", "orchestration_cost", "model_cost", "review_cost", "rework_cost", "implementation_cost", "qualified_evidence", "avoided_labor", "avoided_audit_rework", "expected_loss_reduction", "finance_approved_attributable_margin", "confirmed_contract_value", "modeled_pipeline_influenced"]


def calculate_economics(data: dict[str, Any]) -> dict:
    require_non_negative(data, ECONOMIC_FIELDS)
    qualified = data.get("qualified_evidence", 0)
    operating = sum(data.get(key, 0) for key in ["collector_cost", "storage_cost", "orchestration_cost", "model_cost", "review_cost", "rework_cost"])
    total_cost = operating + data.get("implementation_cost", 0)
    verified_benefit = sum(data.get(key, 0) for key in ["avoided_labor", "avoided_audit_rework", "expected_loss_reduction", "finance_approved_attributable_margin"])
    result = {
        "cost_per_qualified_evidence": round(operating / qualified, 2) if qualified else None,
        "operating_cost": round(operating, 2), "total_cost": round(total_cost, 2),
        "verified_benefit": round(verified_benefit, 2), "net_verified_value": round(verified_benefit - total_cost, 2),
        "roi": round((verified_benefit - total_cost) / total_cost, 4) if total_cost else None,
        "confirmed_contract_value_context_only": data.get("confirmed_contract_value", 0),
        "modeled_pipeline_influenced_context_only": data.get("modeled_pipeline_influenced", 0),
        "finance_approved_attributable_margin": data.get("finance_approved_attributable_margin", 0),
    }
    result["receipt_sha256"] = receipt_sha256(result)
    return result
