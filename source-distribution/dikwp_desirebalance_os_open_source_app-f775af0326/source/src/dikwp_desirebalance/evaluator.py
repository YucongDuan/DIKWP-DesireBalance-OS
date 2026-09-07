from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .models import CompetitionContext, DesireItem
from .scoring import score_desire, score_involution


ROLE_ACTIONS = {
    "individual": [
        "Separate basic needs, capability goals, relational goals, and positional competition.",
        "For high-capture desires, add a cooling interval and define a sufficiency threshold.",
        "Measure debt, time, attention and recovery cost together with purchase price.",
    ],
    "household": [
        "Create a care-time and resilience floor before status-oriented spending.",
        "Replace single-rank education targets with a portfolio of capability and wellbeing goals.",
        "Make debt and comparison pressure visible in household decisions.",
    ],
    "organization": [
        "Reduce rank-only KPIs, forced overtime and repeated internal tournaments.",
        "Reward quality, learning, safety, cooperation, customer value and reusable knowledge.",
        "Publish exit, appeal and workload recovery mechanisms.",
    ],
    "platform": [
        "Audit urgency, infinite-scroll, streak, shame and hidden-retention mechanisms.",
        "Give users an intent reset, easy opt-out and clear commercial sponsorship labels.",
        "Do not sell inferred intentions without specific, revocable consent.",
    ],
    "community": [
        "Expand public cultural, health, education, sport and care services that reduce positional scarcity.",
        "Use capability vouchers and access infrastructure instead of coercive consumption targets.",
        "Track who carries the cost of growth and who can exit a failed policy.",
    ],
    "policy": [
        "Coordinate consumption support with social protection, wage growth and public services.",
        "Treat destructive price wars, forced overtime and rank inflation as system design problems.",
        "Require evidence, review, sunset clauses and distributional analysis for interventions.",
    ],
}


def load_case(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def analyze_case(case: dict[str, Any]) -> dict[str, Any]:
    desire_items = [DesireItem.from_dict(x) for x in case.get("desire_items", [])]
    contexts = [CompetitionContext.from_dict(x) for x in case.get("competition_contexts", [])]
    desire_scores = [score_desire(item) for item in desire_items]
    involution_scores = [score_involution(context) for context in contexts]

    routes = Counter(row["route"] for row in desire_scores)
    actor_types = sorted({row["actor_type"] for row in desire_scores} | {row["actor_type"] for row in involution_scores})
    role_actions = {role: ROLE_ACTIONS.get(role, ROLE_ACTIONS["individual"]) for role in actor_types}

    mean_quality = sum(x["desire_quality_index"] for x in desire_scores) / max(1, len(desire_scores))
    mean_prosperity = sum(x["prosperity_contribution_index"] for x in desire_scores) / max(1, len(desire_scores))
    mean_capture = sum(x["capture_risk_index"] for x in desire_scores) / max(1, len(desire_scores))
    mean_involution = sum(x["involution_pressure_index"] for x in involution_scores) / max(1, len(involution_scores))

    if mean_involution >= 0.62 or mean_capture >= 0.62:
        overall = "structural_redesign_required"
    elif mean_prosperity >= 0.58 and mean_quality >= 0.58:
        overall = "targeted_conversion_pilot_recommended"
    else:
        overall = "human_review_and_local_calibration_required"

    ledger = []
    for item, score in zip(desire_items, desire_scores):
        ledger.append({
            "object_id": item.desire_id,
            "D": {"description": item.description, "intensity": item.intensity},
            "I": {"category": item.category, "actor_type": item.actor_type},
            "K": {"desire_quality_index": score["desire_quality_index"], "capture_risk_index": score["capture_risk_index"]},
            "W": {"externality": item.third_party_externality, "ecological_externality": item.ecological_externality, "reversibility": item.reversibility},
            "P": case.get("purpose_contract", {}),
            "R": {"evidence_strength": item.evidence_strength, "route": score["route"], "residual": "Local calibration required; score is not a diagnosis or moral rank."},
        })

    return {
        "system": "DIKWP DesireBalance OS",
        "version": "0.1.0",
        "case_id": case.get("case_id", "unknown"),
        "title": case.get("title", "Untitled desire economy case"),
        "overall_decision": overall,
        "summary": {
            "desire_count": len(desire_scores),
            "competition_context_count": len(involution_scores),
            "mean_desire_quality_index": round(mean_quality, 4),
            "mean_prosperity_contribution_index": round(mean_prosperity, 4),
            "mean_capture_risk_index": round(mean_capture, 4),
            "mean_involution_pressure_index": round(mean_involution, 4),
            "route_counts": dict(routes),
        },
        "purpose_contract": case.get("purpose_contract", {}),
        "desire_scores": desire_scores,
        "involution_scores": involution_scores,
        "dikwp_ledger": ledger,
        "role_actions": role_actions,
        "residuals": [
            "Weights are local policy parameters, not universal moral constants.",
            "Scores cannot determine a person's worth, eligibility, employment, credit or punishment.",
            "Longitudinal outcomes and distributional effects require external evaluation.",
        ],
        "kill_conditions": [
            "Use of the tool for punitive social scoring or automated eligibility decisions.",
            "Hidden profiling, covert persuasion or sale of inferred intentions without consent.",
            "Removal of evidence, uncertainty, appeal or exit mechanisms.",
        ],
        "recovery_conditions": [
            "Return to aggregate and voluntary analysis.",
            "Restore purpose, evidence, residual and appeal ledgers.",
            "Recalibrate weights with affected stakeholders and publish distributional impacts.",
        ],
    }
