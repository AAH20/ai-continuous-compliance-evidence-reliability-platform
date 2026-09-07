"""SRE-style objectives and evidence error budgets for controls."""

from .canonical import receipt_sha256


def calculate_control_slo(*, required_minutes: float, valid_minutes: float, objective_percent: float, elapsed_fraction: float = 1.0) -> dict:
    if required_minutes <= 0:
        raise ValueError("required_minutes must be positive")
    if not 0 <= valid_minutes <= required_minutes:
        raise ValueError("valid_minutes must be between zero and required_minutes")
    if not 0 < objective_percent < 100:
        raise ValueError("objective_percent must be between zero and 100")
    if not 0 < elapsed_fraction <= 1:
        raise ValueError("elapsed_fraction must be between zero and one")
    availability = valid_minutes / required_minutes
    allowed_bad = required_minutes * (1 - objective_percent / 100)
    consumed_bad = required_minutes - valid_minutes
    expected_consumption = allowed_bad * elapsed_fraction
    burn_rate = consumed_bad / expected_consumption if expected_consumption else float("inf")
    result = {
        "availability_percent": round(availability * 100, 6), "objective_percent": objective_percent,
        "allowed_bad_minutes": round(allowed_bad, 6), "consumed_bad_minutes": round(consumed_bad, 6),
        "remaining_error_budget_minutes": round(max(allowed_bad - consumed_bad, 0), 6),
        "burn_rate": round(burn_rate, 6), "met": availability * 100 >= objective_percent,
        "state": "burning" if burn_rate > 2 else "watch" if burn_rate > 1 else "healthy",
    }
    result["receipt_sha256"] = receipt_sha256(result)
    return result
