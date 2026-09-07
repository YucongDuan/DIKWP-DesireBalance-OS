from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


@dataclass
class DesireItem:
    desire_id: str
    actor_id: str
    actor_type: str
    name: str
    description: str
    category: str
    intensity: float = 0.5
    autonomy: float = 0.5
    basic_need_relevance: float = 0.0
    capability_gain: float = 0.5
    relational_gain: float = 0.3
    innovation_spillover: float = 0.3
    wellbeing_durability: float = 0.4
    reversibility: float = 0.5
    evidence_strength: float = 0.5
    positionality: float = 0.3
    manipulation_pressure: float = 0.2
    debt_burden: float = 0.2
    time_burden: float = 0.2
    ecological_externality: float = 0.2
    third_party_externality: float = 0.2
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DesireItem":
        fields = cls.__dataclass_fields__
        cleaned = {k: v for k, v in data.items() if k in fields}
        return cls(**cleaned)


@dataclass
class CompetitionContext:
    context_id: str
    name: str
    actor_type: str
    relative_rank_dependence: float = 0.5
    winner_take_all: float = 0.4
    effort_escalation: float = 0.5
    marginal_return_decline: float = 0.4
    forced_visibility: float = 0.3
    rule_opacity: float = 0.3
    exit_barrier: float = 0.4
    duplicated_effort: float = 0.4
    price_war_pressure: float = 0.3
    safety_externality: float = 0.2

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompetitionContext":
        fields = cls.__dataclass_fields__
        return cls(**{k: v for k, v in data.items() if k in fields})
