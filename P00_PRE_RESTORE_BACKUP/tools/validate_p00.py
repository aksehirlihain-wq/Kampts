#!/usr/bin/env python3
"""
validate_p00.py — Kampus PTS P00 Quality & Governance Validator

Performs automated checks on:
1. File tree existence
2. Registries schemas, row counts, unique IDs, and honest statuses
3. Feature flags configuration (all live operational flags must be false)
4. JSON schema validity
"""

import csv
import json
import os
import sys
from pathlib import Path


def find_project_root():
    current = Path.cwd()
    if (current / "docs" / "registries").exists():
        return current
    if (current / "KampusPTS" / "docs" / "registries").exists():
        return current / "KampusPTS"
    # fallback to parent directory
    for parent in current.parents:
        if (parent / "KampusPTS" / "docs" / "registries").exists():
            return parent / "KampusPTS"
        if (parent / "docs" / "registries").exists():
            return parent
    return current


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "Directory.Build.props",
    ".editorconfig",
    ".gitignore",
    ".gitattributes",
    "docs/charter.md",
    "docs/financial-authority-matrix.md",
    "docs/governance/foundational-invariants.md",
    "docs/governance/gates.md",
    "docs/governance/raci.md",
    "docs/governance/change-control.md",
    "docs/governance/security-controls.md",
    "docs/governance/quality-scorecard.md",
    "docs/architecture/overview.md",
    "docs/architecture/financial-domain.md",
    "docs/architecture/system-context.mmd",
    "docs/architecture/event-envelope.schema.json",
    "docs/architecture/adr/ADR-001.md",
    "docs/architecture/adr/ADR-002.md",
    "docs/architecture/adr/ADR-003.md",
    "docs/registries/README.md",
    "docs/registries/requirements.csv",
    "docs/registries/nfr.csv",
    "docs/registries/decisions.csv",
    "docs/registries/risks.csv",
    "docs/registries/blockers.csv",
    "docs/registries/traceability.csv",
    "docs/registries/test-cases.csv",
    "docs/registries/gates.csv",
    "docs/templates/REQ-template.md",
    "docs/templates/NFR-template.md",
    "docs/templates/DEC-template.md",
    "docs/templates/ADR-template.md",
    "docs/templates/RISK-template.md",
    "docs/templates/BLK-template.md",
    "docs/templates/TC-template.md",
    "docs/templates/EVD-template.md",
    "docs/templates/CR-template.md",
    "docs/templates/GATE-template.md",
    "docs/templates/BR-template.md",
    "docs/gates/G0-checklist.md",
    "docs/gates/G1-input-checklist.md",
    "docs/gates/P00-delivery-report.md",
    "config/features.example.json",
    "tools/validate_p00.py",
    "tools/build_manifest.py",
    "tests/test_validate_p00.py",
    ".github/workflows/p00-validation.yml",
]


def validate_file_tree(root: Path):
    errors = []
    for rel_path in REQUIRED_FILES:
        full_path = root / rel_path
        if not full_path.exists():
            errors.append(f"Missing required file: {rel_path}")
    return errors


def read_csv_rows(file_path: Path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def validate_registries(root: Path):
    errors = []
    reg_dir = root / "docs" / "registries"

    # 1. requirements.csv (40 items REQ-001..040)
    req_file = reg_dir / "requirements.csv"
    if req_file.exists():
        rows, fields = read_csv_rows(req_file)
        if len(rows) != 40:
            errors.append(f"requirements.csv must have exactly 40 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 40:
            errors.append("Duplicate or missing IDs in requirements.csv")
        for i in range(1, 41):
            expected_id = f"REQ-{i:03d}"
            if expected_id not in ids:
                errors.append(f"Missing ID {expected_id} in requirements.csv")

    # 2. nfr.csv (16 items NFR-001..016)
    nfr_file = reg_dir / "nfr.csv"
    if nfr_file.exists():
        rows, fields = read_csv_rows(nfr_file)
        if len(rows) != 16:
            errors.append(f"nfr.csv must have exactly 16 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 16:
            errors.append("Duplicate or missing IDs in nfr.csv")
        for i in range(1, 17):
            expected_id = f"NFR-{i:03d}"
            if expected_id not in ids:
                errors.append(f"Missing ID {expected_id} in nfr.csv")

    # 3. decisions.csv (31 items DEC-001..031, all DECISION_REQUIRED, TO_ASSIGN, TBD)
    dec_file = reg_dir / "decisions.csv"
    if dec_file.exists():
        rows, fields = read_csv_rows(dec_file)
        if len(rows) != 31:
            errors.append(f"decisions.csv must have exactly 31 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 31:
            errors.append("Duplicate or missing IDs in decisions.csv")
        for r in rows:
            rec_id = r.get("Id", "")
            if r.get("Status") != "DECISION_REQUIRED":
                errors.append(f"{rec_id}: Status must be DECISION_REQUIRED, got {r.get('Status')}")
            if r.get("DecisionMaker") != "TO_ASSIGN":
                errors.append(f"{rec_id}: DecisionMaker must be TO_ASSIGN, got {r.get('DecisionMaker')}")
            if r.get("DecisionDate") != "TBD":
                errors.append(f"{rec_id}: DecisionDate must be TBD, got {r.get('DecisionDate')}")

    # 4. risks.csv (15 items RISK-001..015)
    risk_file = reg_dir / "risks.csv"
    if risk_file.exists():
        rows, fields = read_csv_rows(risk_file)
        if len(rows) != 15:
            errors.append(f"risks.csv must have exactly 15 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 15:
            errors.append("Duplicate or missing IDs in risks.csv")

    # 5. blockers.csv (8 items BLK-001..008, all OPEN)
    blk_file = reg_dir / "blockers.csv"
    if blk_file.exists():
        rows, fields = read_csv_rows(blk_file)
        if len(rows) != 8:
            errors.append(f"blockers.csv must have exactly 8 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 8:
            errors.append("Duplicate or missing IDs in blockers.csv")
        for r in rows:
            if r.get("Status") != "OPEN":
                errors.append(f"{r.get('Id')}: Blocker status must be OPEN, got {r.get('Status')}")

    # 6. test-cases.csv (10 items TC-001..010, all NOT_RUN)
    tc_file = reg_dir / "test-cases.csv"
    if tc_file.exists():
        rows, fields = read_csv_rows(tc_file)
        if len(rows) != 10:
            errors.append(f"test-cases.csv must have exactly 10 rows, found {len(rows)}")
        ids = [r.get("Id") for r in rows]
        if len(set(ids)) != 10:
            errors.append("Duplicate or missing IDs in test-cases.csv")
        for r in rows:
            if r.get("Status") != "NOT_RUN":
                errors.append(f"{r.get('Id')}: Test case status must be NOT_RUN in P00, got {r.get('Status')}")

    # 7. traceability.csv (56 items: 40 REQ + 16 NFR, EvidenceId == NONE)
    tr_file = reg_dir / "traceability.csv"
    if tr_file.exists():
        rows, fields = read_csv_rows(tr_file)
        if len(rows) != 56:
            errors.append(f"traceability.csv must have exactly 56 rows (40 REQ + 16 NFR), found {len(rows)}")
        req_ids = [r.get("RequirementId") for r in rows]
        if len(set(req_ids)) != 56:
            errors.append("Duplicate or missing RequirementId in traceability.csv")
        for r in rows:
            if r.get("EvidenceId") != "NONE":
                errors.append(f"{r.get('RequirementId')}: Real evidence must be NONE in P00, got {r.get('EvidenceId')}")

    # 8. gates.csv (10 gates G0..G9, G0 == NOT_APPROVED, G1..G9 == NOT_STARTED)
    gate_file = reg_dir / "gates.csv"
    if gate_file.exists():
        rows, fields = read_csv_rows(gate_file)
        if len(rows) != 10:
            errors.append(f"gates.csv must have exactly 10 rows (G0..G9), found {len(rows)}")
        for r in rows:
            gid = r.get("GateId")
            if gid == "G0":
                if r.get("Status") != "NOT_APPROVED":
                    errors.append(f"Gate G0 status must be NOT_APPROVED, got {r.get('Status')}")
            else:
                if r.get("Status") != "NOT_STARTED":
                    errors.append(f"Gate {gid} status must be NOT_STARTED in P00, got {r.get('Status')}")

    return errors


def validate_config(root: Path):
    errors = []
    cfg_file = root / "config" / "features.example.json"
    if not cfg_file.exists():
        return ["config/features.example.json missing"]

    try:
        with open(cfg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        flags = data.get("flags", {})
        live_flags = [
            "enable_real_barrier_commands",
            "enable_psp_live_capture",
            "enable_einvoice_live_issuance",
            "enable_erp_live_posting",
            "enable_split_settlement_live",
            "enable_safety_interlock_bypass",
        ]
        for lf in live_flags:
            if flags.get(lf) is not False:
                errors.append(f"Feature flag {lf} must be strictly FALSE in P00 config")
    except Exception as e:
        errors.append(f"Failed parsing config/features.example.json: {e}")

    # Also check event-envelope.schema.json
    envelope_file = root / "docs" / "architecture" / "event-envelope.schema.json"
    if envelope_file.exists():
        try:
            with open(envelope_file, "r", encoding="utf-8") as f:
                env_data = json.load(f)
            required = env_data.get("required", [])
            expected_fields = [
                "eventId", "eventType", "schemaVersion", "occurredAtUtc",
                "receivedAtUtc", "sourceSystem", "correlationId", "causationId",
                "idempotencyKey", "payloadHash", "tenantId", "legalEntityId", "payload"
            ]
            for ef in expected_fields:
                if ef not in required:
                    errors.append(f"event-envelope.schema.json missing required field: {ef}")
        except Exception as e:
            errors.append(f"Failed parsing event-envelope.schema.json: {e}")

    return errors


def run_validation():
    root = find_project_root()
    print(f"=== Kampüs PTS P00 Kalite Doğrulama ===")
    print(f"Proje Dizini: {root}")

    tree_errors = validate_file_tree(root)
    reg_errors = validate_registries(root)
    cfg_errors = validate_config(root)

    total_errors = tree_errors + reg_errors + cfg_errors

    print(f"1. Dosya Ağacı Kontrolü: {'BAŞARILI' if not tree_errors else f'{len(tree_errors)} HATA'}")
    for err in tree_errors:
        print(f"   [FAIL] {err}")

    print(f"2. Kütük ve Sayım Bütünlüğü: {'BAŞARILI' if not reg_errors else f'{len(reg_errors)} HATA'}")
    for err in reg_errors:
        print(f"   [FAIL] {err}")

    print(f"3. Yapılandırma ve Şema Güvenliği: {'BAŞARILI' if not cfg_errors else f'{len(cfg_errors)} HATA'}")
    for err in cfg_errors:
        print(f"   [FAIL] {err}")

    print("-" * 50)
    if not total_errors:
        print("SONUÇ: P00 DOĞRULAMA TAMAMEN BAŞARILI (EXECUTED_PASS)")
        print("Bilgi Durumu: G0=NOT_APPROVED, 31 DECISION_REQUIRED, 8 OPEN BLOCKERS")
        return 0
    else:
        print(f"SONUÇ: P00 DOĞRULAMA BAŞARISIZ ({len(total_errors)} hata)")
        return 1


if __name__ == "__main__":
    sys.exit(run_validation())
