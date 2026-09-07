from __future__ import annotations

import argparse
import json

from .evaluator import analyze_case, load_case
from .reports import write_outputs
from .static_audit import write_audit


def main() -> int:
    parser = argparse.ArgumentParser(prog="desirebalance", description="DIKWP desire metrology and anti-involution toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze a multi-actor desire economy case")
    analyze.add_argument("input")
    analyze.add_argument("--out", required=True)

    audit = sub.add_parser("static-audit", help="Audit the offline source tree")
    audit.add_argument("root")
    audit.add_argument("--out", required=True)

    args = parser.parse_args()
    if args.command == "analyze":
        report = analyze_case(load_case(args.input))
        write_outputs(report, args.out)
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        return 0
    report = write_audit(args.root, args.out)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
