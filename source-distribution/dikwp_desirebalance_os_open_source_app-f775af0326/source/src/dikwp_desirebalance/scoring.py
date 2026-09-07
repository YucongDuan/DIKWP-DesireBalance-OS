from __future__ import annotations

from .models import CompetitionContext, DesireItem, clamp


POSITIVE_WEIGHTS = {
    "autonomy": 0.16,
    "basic_need_relevance": 0.14,
    "capability_gain": 0.16,
    "relational_gain": 0.10,
    "innovation_spillover": 0.10,
    "wellbeing_durability": 0.14,
    "reversibility": 0.10,
    "evidence_strength": 0.10,
}

NEGATIVE_WEIGHTS = {
    "positionality": 0.19,
    "manipulation_pressure": 0.18,
    "debt_burden": 0.16,
    "time_burden": 0.14,
    "ecological_externality": 0.15,
    "third_party_externality": 0.18,
}

INVOLUTION_WEIGHTS = {
    "relative_rank_dependence": 0.16,
    "winner_take_all": 0.13,
    "effort_escalation": 0.16,
    "marginal_return_decline": 0.14,
    "forced_visibility": 0.09,
    "rule_opacity": 0.09,
    "exit_barrier": 0.10,
    "duplicated_effort": 0.07,
    "price_war_pressure": 0.04,
    "safety_externality": 0.02,
}


def weighted(item: object, weights: dict[str, float]) -> float:
    return sum(clamp(getattr(item, name, 0.0)) * weight for name, weight in weights.items())


def score_desire(item: DesireItem) -> dict:
    positive = weighted(item, POSITIVE_WEIGHTS)
    burden = weighted(item, NEGATIVE_WEIGHTS)
    quality = clamp(0.55 + positive * 0.75 - burden * 0.85)
    prosperity = clamp(
        0.12
        + 0.20 * item.basic_need_relevance
        + 0.24 * item.capability_gain
        + 0.18 * item.innovation_spillover
        + 0.15 * item.relational_gain
        + 0.14 * item.wellbeing_durability
        - 0.12 * item.ecological_externality
        - 0.11 * item.third_party_externality
    )
    capture = clamp(
        0.34 * item.positionality
        + 0.32 * item.manipulation_pressure
        + 0.17 * item.debt_burden
        + 0.10 * item.time_burden
        + 0.07 * (1.0 - item.autonomy)
    )
    sufficiency_gap = clamp(1.0 - max(item.basic_need_relevance, item.wellbeing_durability))

    if item.basic_need_relevance >= 0.75 and burden <= 0.55:
        route = "protect_and_expand_basic_capability"
    elif quality >= 0.68 and prosperity >= 0.60 and capture < 0.45:
        route = "support_and_expand"
    elif capture >= 0.72 or (item.debt_burden >= 0.75 and item.positionality >= 0.55):
        route = "cool_and_reframe"
    elif item.third_party_externality >= 0.80 or item.manipulation_pressure >= 0.90:
        route = "human_or_policy_review"
    else:
        route = "redesign_and_pilot"

    return {
        "desire_id": item.desire_id,
        "actor_id": item.actor_id,
        "actor_type": item.actor_type,
        "name": item.name,
        "category": item.category,
        "desire_quality_index": round(quality, 4),
        "prosperity_contribution_index": round(prosperity, 4),
        "capture_risk_index": round(capture, 4),
        "sufficiency_gap_proxy": round(sufficiency_gap, 4),
        "route": route,
    }


def score_involution(context: CompetitionContext) -> dict:
    score = weighted(context, INVOLUTION_WEIGHTS)
    if score >= 0.72:
        grade = "I4 Severe Involution Pressure"
    elif score >= 0.56:
        grade = "I3 High Involution Pressure"
    elif score >= 0.40:
        grade = "I2 Material Involution Pressure"
    elif score >= 0.24:
        grade = "I1 Emerging Involution Pressure"
    else:
        grade = "I0 Low Involution Pressure"
    return {
        "context_id": context.context_id,
        "name": context.name,
        "actor_type": context.actor_type,
        "involution_pressure_index": round(score, 4),
        "grade": grade,
    }
