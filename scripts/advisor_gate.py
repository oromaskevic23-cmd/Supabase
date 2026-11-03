#!/usr/bin/env python3
"""Offline, fail-closed review of sanitized Supabase advisor summaries.

This tool NEVER contacts a database, changes permissions, or proves tenant isolation.
Input is an explicitly curated metadata-only snapshot; do not paste raw findings.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

KEYS = {"schema_version", "observed_at_utc", "security", "performance"}
LEVELS = {"INFO", "WARN", "ERROR"}
ITEM_KEYS = {"name", "level", "count"}
NAME = re.compile(r"^[a-z][a-z0-9_]{0,127}$")


class SnapshotError(ValueError):
    """Snapshot is missing mandatory evidence or violates the safe schema."""


def evaluate(snapshot):
    if not isinstance(snapshot, dict) or set(snapshot) != KEYS:
        raise SnapshotError("Expected exactly schema_version, observed_at_utc, security, performance")
    if type(snapshot["schema_version"]) is not int or snapshot["schema_version"] != 1:
        raise SnapshotError("Unsupported schema_version")
    stamp = snapshot["observed_at_utc"]
    if not isinstance(stamp, str):
        raise SnapshotError("observed_at_utc must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SnapshotError("Invalid observation timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SnapshotError("Timestamp must include a UTC offset")

    findings = []
    seen = set()
    for domain in ("security", "performance"):
        records = snapshot[domain]
        if not isinstance(records, list):
            raise SnapshotError(f"{domain} must be a list")
        for item in records:
            if not isinstance(item, dict) or set(item) != ITEM_KEYS:
                raise SnapshotError(f"{domain} record has missing/extra fields")
            name, level, count = item["name"], item["level"], item["count"]
            if not isinstance(name, str) or not NAME.fullmatch(name):
                raise SnapshotError(f"Invalid {domain} advisor name")
            if level not in LEVELS:
                raise SnapshotError(f"Invalid severity for {name}")
            if type(count) is not int or count < 0:
                raise SnapshotError(f"Invalid finding count for {name}")
            if (domain, name) in seen:
                raise SnapshotError(f"Duplicate advisor type: {domain}/{name}")
            seen.add((domain, name))
            if count == 0:
                continue
            disposition = "BLOCK" if level == "ERROR" or (domain == "security" and level == "WARN") else "REVIEW"
            findings.append({"domain": domain, "name": name, "level": level,
                             "count": count, "disposition": disposition})

    blocks = [item for item in findings if item["disposition"] == "BLOCK"]
    status = "BLOCK" if blocks else ("REVIEW" if findings else "NO_FINDINGS_REPORTED")
    return {
        "gate": status,
        "observed_at_utc": stamp,
        "source": "MANUALLY_SANITIZED_SUPABASE_ADVISORS_NOT_LIVE",
        "blocking_types": len(blocks),
        "review_types": len(findings) - len(blocks),
        "findings": findings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Sanitized metadata-only advisor JSON")
    args = parser.parse_args(argv)
    try:
        report = evaluate(json.loads(args.snapshot.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, SnapshotError) as exc:
        print(f"ADVISOR_GATE_INVALID_INPUT: {exc}", file=sys.stderr)
        return 3
    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if report["gate"] == "BLOCK" else 0


if __name__ == "__main__":
    sys.exit(main())
