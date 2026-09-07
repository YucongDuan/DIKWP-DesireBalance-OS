from pathlib import Path

from dikwp_desirebalance.evaluator import analyze_case, load_case
from dikwp_desirebalance.static_audit import audit_tree

ROOT = Path(__file__).resolve().parents[1]


def test_demo_case_has_expected_routes():
    report = analyze_case(load_case(ROOT / "examples" / "sample_multirole_case.json"))
    routes = {row["desire_id"]: row["route"] for row in report["desire_scores"]}
    assert routes["d1"] in {"support_and_expand", "protect_and_expand_basic_capability"}
    assert routes["d4"] in {"cool_and_reframe", "human_or_policy_review"}


def test_involution_context_is_detected():
    report = analyze_case(load_case(ROOT / "examples" / "sample_multirole_case.json"))
    values = {row["context_id"]: row["involution_pressure_index"] for row in report["involution_scores"]}
    assert values["c1"] > 0.65
    assert values["c3"] < values["c1"]


def test_static_audit_passes():
    result = audit_tree(ROOT / "src")
    assert result["pass"] is True
