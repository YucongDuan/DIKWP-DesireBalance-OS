from __future__ import annotations

import ast
import json
from pathlib import Path

FORBIDDEN_IMPORTS = {"requests", "httpx", "urllib", "socket", "subprocess", "selenium", "playwright", "paramiko"}
FORBIDDEN_TEXT = {"credential capture", "hidden telemetry", "automatic denial", "social credit score"}


def audit_tree(root: str | Path) -> dict:
    root_path = Path(root)
    findings = []
    for path in root_path.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            findings.append({"file": str(path), "type": "syntax_error", "detail": str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                        findings.append({"file": str(path), "type": "forbidden_import", "detail": alias.name})
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                    findings.append({"file": str(path), "type": "forbidden_import", "detail": node.module})
        lowered = text.lower()
        for term in FORBIDDEN_TEXT:
            if term in lowered and path.name != "static_audit.py":
                findings.append({"file": str(path), "type": "forbidden_text", "detail": term})
    return {
        "policy": "No network clients, browser automation, subprocess, credential capture, hidden telemetry, punitive social scoring, or automated denial in the offline core.",
        "pass": not findings,
        "finding_count": len(findings),
        "findings": findings,
    }


def write_audit(root: str | Path, output: str | Path) -> dict:
    report = audit_tree(root)
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
