#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

MUTABLE_REFS = {"main", "master", "dev", "develop", "latest"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


@dataclass
class Finding:
    bucket: str
    title: str
    detail: str


@dataclass
class Report:
    repoName: str
    score: int
    counts: dict[str, int]
    findings: list[Finding]


def add_finding(findings: list[Finding], bucket: str, title: str, detail: str) -> None:
    findings.append(Finding(bucket=bucket, title=title, detail=detail))


def score_from_findings(findings: list[Finding]) -> int:
    score = 100
    for finding in findings:
        if finding.bucket == "fixNow":
            score -= 25
        elif finding.bucket == "warning":
            score -= 10
    return max(0, score)


def parse_workflow_text(text: str, workflow_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    doc = yaml.safe_load(text) or {}

    # Check for overprivileged pull_request_target trigger.
    on_value = doc.get("on")
    triggers: set[str] = set()
    if isinstance(on_value, str):
        triggers.add(on_value)
    elif isinstance(on_value, list):
        triggers.update(str(item) for item in on_value)
    elif isinstance(on_value, dict):
        triggers.update(str(k) for k in on_value.keys())

    if "pull_request_target" in triggers:
        add_finding(
            findings,
            "fixNow",
            "Overprivileged trigger",
            f"{workflow_path} uses pull_request_target. Switch to pull_request unless write access is required.",
        )

    # Focus on checkout steps in this workflow.
    for job in (doc.get("jobs") or {}).values():
        if not isinstance(job, dict):
            continue
        for idx, step in enumerate(job.get("steps") or [], start=1):
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", "")).strip()
            if not uses.startswith("actions/checkout@"):
                continue
            step_name = str(step.get("name", f"step #{idx}"))
            with_cfg = step.get("with") or {}
            ref = with_cfg.get("ref")
            persist = str(with_cfg.get("persist-credentials")).strip().lower() if "persist-credentials" in with_cfg else None
            depth = str(with_cfg.get("fetch-depth")).strip() if "fetch-depth" in with_cfg else None

            if ref is not None:
                cleaned_ref = str(ref).strip().strip("'\"")
                if cleaned_ref.startswith("${{"):
                    continue
                if cleaned_ref in MUTABLE_REFS or not SHA_RE.fullmatch(cleaned_ref):
                    add_finding(
                        findings,
                        "fixNow",
                        f"Mutable checkout ref in {step_name}",
                        f"{workflow_path} checks out {cleaned_ref!r}. Pin third-party repos to an immutable commit SHA.",
                    )

            if persist != "false":
                add_finding(
                    findings,
                    "warning",
                    f"Persistent credentials in {step_name}",
                    f"{workflow_path} should set persist-credentials: false on checkout steps that do not need git auth.",
                )

            if depth == "0":
                add_finding(
                    findings,
                    "warning",
                    f"Unnecessary full clone in {step_name}",
                    f"{workflow_path} uses fetch-depth: 0. Shallow checkout is enough for this workflow.",
                )

    if not findings:
        add_finding(
            findings,
            "good",
            "Workflow hygiene looks good",
            f"{workflow_path} has pinned actions, least-privilege trigger, and no obvious checkout issues.",
        )

    return findings


def build_report(repo_root: Path) -> Report:
    workflow_path = repo_root / ".github" / "workflows" / "agent-hygiene-review.yml"
    text = workflow_path.read_text()
    findings = parse_workflow_text(text, workflow_path)
    counts = {
        "good": sum(1 for finding in findings if finding.bucket == "good"),
        "warning": sum(1 for finding in findings if finding.bucket == "warning"),
        "fixNow": sum(1 for finding in findings if finding.bucket == "fixNow"),
    }
    score = score_from_findings(findings)
    return Report(repoName=repo_root.name, score=score, counts=counts, findings=findings)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--min-score", type=int, default=75)
    args = parser.parse_args()

    report = build_report(args.repo_root)
    print(json.dumps(asdict(report), indent=2))
    return 1 if report.score < args.min_score else 0


if __name__ == "__main__":
    raise SystemExit(main())
