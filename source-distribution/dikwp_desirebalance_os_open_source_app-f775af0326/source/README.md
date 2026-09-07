# DIKWP DesireBalance OS

**Desire metrology, sustainable prosperity conversion, and anti-involution planning.**

DIKWP DesireBalance OS is an offline-first reference system for analyzing the tension between desire-driven prosperity and destructive involution. It does not suppress desire or rank people. It distinguishes basic needs, capability-expanding desires, relational and creative desires, positional competition, manipulative capture, debt/time burdens and externalities.

## Why

Modern economies need demand, aspiration, entrepreneurship and innovation. The same mechanisms can also produce status arms races, overwork, credential inflation, price wars, attention capture, debt stress and ecological cost. The project uses DIKWP-Mesh SemanticClosure to make those trade-offs explicit.

## Core outputs

- Desire portfolio and DIKWP ledger
- Desire Quality Index, Prosperity Contribution Index and Capture Risk Index
- Involution Pressure Matrix
- Purpose Contract
- Role-specific action plans
- Organization KPI reform plan
- Platform manipulation audit
- Community and policy option set

## Quick start

```bash
pip install -e .
desirebalance analyze examples/sample_multirole_case.json --out outputs/demo
desirebalance static-audit src --out outputs/demo/static_boundary_audit_report.json
```

Optional UI:

```bash
pip install -e .[app]
streamlit run src/dikwp_desirebalance/app.py
```

## Boundaries

This project is not a social credit system, diagnostic system, eligibility engine, employee ranking system, financial adviser or enforcement tool. Scores are local, contestable and reversible. They cannot determine a person's worth or rights.

## Attribution

Please retain attribution to **Yucong Duan / DIKWP** and the included `NOTICE` and `CITATION.cff` files.
