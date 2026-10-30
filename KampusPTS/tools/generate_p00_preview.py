#!/usr/bin/env python3
"""
generate_p00_preview.py — Derives preview snapshot directly from canonical registries.
Outputs src/data/p00-canonical.json for the read-only React preview.
"""

import csv
import json
import os
import sys
from pathlib import Path


def find_workspace_root():
    current = Path.cwd()
    if (current / "KampusPTS").exists():
        return current
    if current.name == "KampusPTS":
        return current.parent
    return current


def read_csv(path: Path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def generate_preview():
    ws_root = find_workspace_root()
    kampus_dir = ws_root / "KampusPTS"
    reg_dir = kampus_dir / "docs" / "registries"

    reqs = read_csv(reg_dir / "requirements.csv")
    nfrs = read_csv(reg_dir / "nfr.csv")
    decs = read_csv(reg_dir / "decisions.csv")
    risks = read_csv(reg_dir / "risks.csv")
    blks = read_csv(reg_dir / "blockers.csv")
    tcs = read_csv(reg_dir / "test-cases.csv")
    trace = read_csv(reg_dir / "traceability.csv")
    gates = read_csv(reg_dir / "gates.csv")

    preview_data = {
        "version": "1.2_canonical",
        "phase": "P00",
        "governance_status": "G0_NOT_APPROVED",
        "technical_status": "P00_SOURCE_READY",
        "counts": {
            "requirements": len(reqs),
            "nfr": len(nfrs),
            "decisions": len(decs),
            "risks": len(risks),
            "blockers": len(blks),
            "test_cases": len(tcs),
            "traceability": len(trace),
            "gates": len(gates),
        },
        "sample_records": {
            "req_001": next(r for r in reqs if r["id"] == "REQ-001"),
            "req_002": next(r for r in reqs if r["id"] == "REQ-002"),
            "nfr_001": next(n for n in nfrs if n["id"] == "NFR-001"),
            "dec_001": next(d for d in decs if d["id"] == "DEC-001"),
            "dec_002": next(d for d in decs if d["id"] == "DEC-002"),
        },
        "blockers": blks,
        "gates": gates,
        "features": {
            "gateRealCommandsEnabled": False,
            "paymentRealCaptureEnabled": False,
            "eDocumentRealIssueEnabled": False,
            "erpRealPostingEnabled": False,
            "multiEntitySplitSettlementEnabled": False,
        },
    }

    out_dir = ws_root / "src" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "p00-canonical.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(preview_data, f, ensure_ascii=False, indent=2)

    print(f"Generated preview snapshot: {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(generate_preview())
