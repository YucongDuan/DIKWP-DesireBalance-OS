from __future__ import annotations

import csv
import json
from pathlib import Path


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(report: dict, section: str) -> str:
    title = report.get("title", "DIKWP DesireBalance")
    if section == "prosperity":
        lines = [f"# Sustainable Prosperity Conversion Plan: {title}", ""]
        for row in report["desire_scores"]:
            lines += [f"## {row['name']}", f"- Route: `{row['route']}`", f"- Desire quality: {row['desire_quality_index']}", f"- Prosperity contribution: {row['prosperity_contribution_index']}", f"- Capture risk: {row['capture_risk_index']}", ""]
        lines += ["## Operational principle", "Expand desires that improve capability, durable wellbeing and shared value. Redesign desires dominated by positional competition, manipulation, debt or third-party externalities."]
        return "\n".join(lines)
    if section == "roles":
        lines = [f"# Role-Specific Action Plans: {title}", ""]
        for role, actions in report["role_actions"].items():
            lines.append(f"## {role}")
            lines.extend(f"- {action}" for action in actions)
            lines.append("")
        return "\n".join(lines)
    if section == "kpi":
        return """# Organization KPI Reform Plan

- Replace single ranking with a balanced set: quality, safety, learning, cooperation, customer value and recovery.
- Separate exploration from production targets.
- Audit overtime, internal tournaments and duplicated reporting as externalized costs.
- Publish appeal, workload recovery and exit routes.
- Do not use DesireBalance scores for individual punishment, dismissal, pay or promotion.
"""
    if section == "platform":
        return """# Platform Manipulation Audit

Audit the following mechanisms before launch:

- Artificial scarcity and countdown pressure.
- Infinite scroll, streak loss and variable reward loops.
- Confirm-shaming and difficult cancellation.
- Hidden sponsored ranking or intent brokering.
- Default data retention and hard-to-find opt-out.
- Personalized persuasion using sensitive inferred traits.

Required controls: explicit purpose, revocable consent, intent reset, easy exit, provenance, independent review and user-accessible audit history.
"""
    if section == "policy":
        return """# Community and Policy Option Set

1. Increase income security and portable social protection so households do not rely on status competition for security.
2. Expand high-quality public services, cultural facilities, sports, care and lifelong education.
3. Use temporary, evidence-based demand support for capability-enhancing and service consumption.
4. Address destructive price wars, delayed supplier payments and unsafe cost cutting.
5. Reform evaluation systems that create rank scarcity without increasing real capability.
6. Require sunset clauses, distributional analysis, appeal and independent evaluation.
"""
    return "# Recommendations\n\nSee generated scorecards and action plans.\n"


def write_outputs(report: dict, out_dir: str | Path) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "desirebalance_report.json", report)
    write_json(out / "purpose_contract.json", report.get("purpose_contract", {}))
    write_json(out / "desire_metrology_ledger.json", report.get("dikwp_ledger", []))
    write_csv(out / "desire_portfolio.csv", report.get("desire_scores", []))
    write_csv(out / "involution_pressure_matrix.csv", report.get("involution_scores", []))
    (out / "prosperity_conversion_plan.md").write_text(render_markdown(report, "prosperity"), encoding="utf-8")
    (out / "role_specific_action_plans.md").write_text(render_markdown(report, "roles"), encoding="utf-8")
    (out / "organization_kpi_reform_plan.md").write_text(render_markdown(report, "kpi"), encoding="utf-8")
    (out / "platform_manipulation_audit.md").write_text(render_markdown(report, "platform"), encoding="utf-8")
    (out / "community_policy_option_set.md").write_text(render_markdown(report, "policy"), encoding="utf-8")
