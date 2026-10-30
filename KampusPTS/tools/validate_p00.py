#!/usr/bin/env python3
"""
validate_p00.py — Kampus PTS P00 Canonical Quality & Governance Validator

Performs automated canonical validation on:
1. File tree existence (49 P00 working files)
2. Canonical Registries schemas, row counts, unique IDs, semantic invariants, and honest statuses
3. Feature flags canonical configuration (features.* live flags strictly false)
4. JSON schema validity for event-envelope and configuration
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
    "docs/reviews/P00-correction-2026-10-30.md",
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

    # 1. requirements.csv (40 items REQ-001..040, status=DESIGNED, canonical columns)
    req_file = reg_dir / "requirements.csv"
    if req_file.exists():
        rows, fields = read_csv_rows(req_file)
        if len(rows) != 40:
            errors.append(f"requirements.csv must have exactly 40 rows, found {len(rows)}")
        expected_cols = {"id", "phase", "title", "requirement", "acceptance", "status", "owner_role", "gate"}
        if not expected_cols.issubset(set(fields or [])):
            errors.append(f"requirements.csv columns must match canonical schema {expected_cols}, got {fields}")
        ids = [r.get("id") for r in rows]
        if len(set(ids)) != 40:
            errors.append("Duplicate or missing IDs in requirements.csv")
        for i in range(1, 41):
            expected_id = f"REQ-{i:03d}"
            if expected_id not in ids:
                errors.append(f"Missing ID {expected_id} in requirements.csv")
        for r in rows:
            if r.get("status") != "DESIGNED":
                errors.append(f"{r.get('id')}: status must be DESIGNED (no fictitious APPROVED), got {r.get('status')}")
        req1 = next((r for r in rows if r.get("id") == "REQ-001"), None)
        if req1 and "Kapsam" not in req1.get("title", ""):
            errors.append(f"REQ-001 title must be canonical scope/governance title, got {req1.get('title')}")

    # 2. nfr.csv (16 items NFR-001..016, status=NOT_RUN)
    nfr_file = reg_dir / "nfr.csv"
    if nfr_file.exists():
        rows, fields = read_csv_rows(nfr_file)
        if len(rows) != 16:
            errors.append(f"nfr.csv must have exactly 16 rows, found {len(rows)}")
        ids = [r.get("id") for r in rows]
        if len(set(ids)) != 16:
            errors.append("Duplicate or missing IDs in nfr.csv")
        for i in range(1, 17):
            expected_id = f"NFR-{i:03d}"
            if expected_id not in ids:
                errors.append(f"Missing ID {expected_id} in nfr.csv")
        for r in rows:
            stat = r.get("verification") or r.get("status")
            if stat != "NOT_RUN":
                errors.append(f"{r.get('id')}: status/verification must be NOT_RUN in P00, got {stat}")
        nfr1 = next((r for r in rows if r.get("id") == "NFR-001"), None)
        if nfr1 and "Kimlik" not in nfr1.get("title", ""):
            errors.append(f"NFR-001 must be canonical Identity/Session security, got {nfr1.get('title')}")

    # 3. decisions.csv (31 items DEC-001..031, all DECISION_REQUIRED, actual_owner=TO_ASSIGN, due_date=TBD, evidence=NONE)
    dec_file = reg_dir / "decisions.csv"
    if dec_file.exists():
        rows, fields = read_csv_rows(dec_file)
        if len(rows) != 31:
            errors.append(f"decisions.csv must have exactly 31 rows, found {len(rows)}")
        expected_cols = {"id", "phase", "title", "options", "status", "actual_owner", "due_date", "evidence"}
        if not expected_cols.issubset(set(fields or [])):
            errors.append(f"decisions.csv columns must match canonical schema, got {fields}")
        ids = [r.get("id") for r in rows]
        if len(set(ids)) != 31:
            errors.append("Duplicate or missing IDs in decisions.csv")
        for r in rows:
            rec_id = r.get("id", "")
            if r.get("status") != "DECISION_REQUIRED":
                errors.append(f"{rec_id}: status must be DECISION_REQUIRED, got {r.get('status')}")
            if r.get("actual_owner") != "TO_ASSIGN":
                errors.append(f"{rec_id}: actual_owner must be TO_ASSIGN, got {r.get('actual_owner')}")
            if r.get("due_date") != "TBD":
                errors.append(f"{rec_id}: due_date must be TBD, got {r.get('due_date')}")
            if r.get("evidence") != "NONE":
                errors.append(f"{rec_id}: evidence must be NONE, got {r.get('evidence')}")
        dec1 = next((r for r in rows if r.get("id") == "DEC-001"), None)
        if dec1:
            opts = dec1.get("options", "")
            for model in ["A Üniversite", "B Döner sermaye", "C Özel işletmeci", "D Çoklu tüzel kişilik"]:
                if model not in opts:
                    errors.append(f"DEC-001 options must include canonical model '{model}'")

    # 4. risks.csv (15 items RISK-001..015, status=OPEN_ASSUMED)
    risk_file = reg_dir / "risks.csv"
    if risk_file.exists():
        rows, fields = read_csv_rows(risk_file)
        if len(rows) != 15:
            errors.append(f"risks.csv must have exactly 15 rows, found {len(rows)}")
        ids = [r.get("id") for r in rows]
        if len(set(ids)) != 15:
            errors.append("Duplicate or missing IDs in risks.csv")
        for r in rows:
            if r.get("status") != "OPEN_ASSUMED":
                errors.append(f"{r.get('id')}: status must be OPEN_ASSUMED, got {r.get('status')}")

    # 5. blockers.csv (8 items BLK-001..008, all OPEN, canonical columns)
    blk_file = reg_dir / "blockers.csv"
    if blk_file.exists():
        rows, fields = read_csv_rows(blk_file)
        if len(rows) != 8:
            errors.append(f"blockers.csv must have exactly 8 rows, found {len(rows)}")
        expected_cols = {"id", "phase", "title", "decision_ids", "requirement_ids", "gates", "blocks", "status"}
        if not expected_cols.issubset(set(fields or [])):
            errors.append(f"blockers.csv columns must match canonical schema, got {fields}")
        for r in rows:
            if r.get("status") != "OPEN":
                errors.append(f"{r.get('id')}: blocker status must be OPEN, got {r.get('status')}")

    # 6. test-cases.csv (10 items TC-001..010, all NOT_RUN, evidence=NONE)
    tc_file = reg_dir / "test-cases.csv"
    if tc_file.exists():
        rows, fields = read_csv_rows(tc_file)
        if len(rows) != 10:
            errors.append(f"test-cases.csv must have exactly 10 rows, found {len(rows)}")
        for r in rows:
            if r.get("status") != "NOT_RUN":
                errors.append(f"{r.get('id')}: test case status must be NOT_RUN, got {r.get('status')}")
            if r.get("evidence") != "NONE":
                errors.append(f"{r.get('id')}: evidence must be NONE, got {r.get('evidence')}")

    # 7. traceability.csv (56 items: 40 REQ + 16 NFR, status=DESIGNED_NOT_TESTED, evidence_id=NONE)
    tr_file = reg_dir / "traceability.csv"
    if tr_file.exists():
        rows, fields = read_csv_rows(tr_file)
        if len(rows) != 56:
            errors.append(f"traceability.csv must have exactly 56 rows (40 REQ + 16 NFR), found {len(rows)}")
        for r in rows:
            if r.get("status") != "DESIGNED_NOT_TESTED":
                errors.append(f"{r.get('requirement_id')}: status must be DESIGNED_NOT_TESTED, got {r.get('status')}")
            if r.get("evidence_id") != "NONE":
                errors.append(f"{r.get('requirement_id')}: evidence_id must be NONE in P00, got {r.get('evidence_id')}")

    # 8. gates.csv (10 gates G0..G9, G0 == NOT_APPROVED, G1..G9 == NOT_STARTED, canonical phase ranges)
    gate_file = reg_dir / "gates.csv"
    if gate_file.exists():
        rows, fields = read_csv_rows(gate_file)
        if len(rows) != 10:
            errors.append(f"gates.csv must have exactly 10 rows (G0..G9), found {len(rows)}")
        for r in rows:
            gid = r.get("id")
            if gid == "G0":
                if r.get("status") != "NOT_APPROVED":
                    errors.append(f"Gate G0 status must be NOT_APPROVED, got {r.get('status')}")
                if r.get("phase_range") != "P00":
                    errors.append(f"Gate G0 phase must be P00, got {r.get('phase_range')}")
            elif gid == "G1":
                if "P01" not in r.get("phase_range", "") or "P04" not in r.get("phase_range", ""):
                    errors.append(f"Gate G1 phase_range must be P01–P04, got {r.get('phase_range')}")
                if r.get("status") != "NOT_STARTED":
                    errors.append(f"Gate G1 status must be NOT_STARTED, got {r.get('status')}")
            elif gid == "G9":
                if "P32" not in r.get("phase_range", "") or "P33" not in r.get("phase_range", ""):
                    errors.append(f"Gate G9 phase_range must be P32–P33, got {r.get('phase_range')}")
            else:
                if r.get("status") != "NOT_STARTED":
                    errors.append(f"Gate {gid} status must be NOT_STARTED in P00, got {r.get('status')}")

    return errors


def validate_config(root: Path):
    errors = []
    cfg_file = root / "config" / "features.example.json"
    if not cfg_file.exists():
        return ["config/features.example.json missing"]

    try:
        with open(cfg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for expected_key in ["environment", "features", "safety", "testData"]:
            if expected_key not in data:
                errors.append(f"config/features.example.json missing canonical root key: {expected_key}")

        features = data.get("features", {})
        live_flags = [
            "gateRealCommandsEnabled",
            "paymentRealCaptureEnabled",
            "eDocumentRealIssueEnabled",
            "erpRealPostingEnabled",
            "multiEntitySplitSettlementEnabled",
        ]
        for lf in live_flags:
            if features.get(lf) is not False:
                errors.append(f"Canonical feature flag '{lf}' must be strictly FALSE in P00 config")

        safety = data.get("safety", {})
        if safety.get("hardwareSafetyInterlockOverride") is not False:
            errors.append("safety.hardwareSafetyInterlockOverride must be strictly FALSE")
    except Exception as e:
        errors.append(f"Failed parsing config/features.example.json: {e}")

    # Envelope schema
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
    print("=== Kampüs PTS P00 Kanonik Kalite Doğrulama ===")
    print(f"Proje Dizini: {root}")

    tree_errors = validate_file_tree(root)
    reg_errors = validate_registries(root)
    cfg_errors = validate_config(root)

    total_errors = tree_errors + reg_errors + cfg_errors

    print(f"1. Dosya Ağacı Kontrolü: {'BAŞARILI' if not tree_errors else f'{len(tree_errors)} HATA'}")
    for err in tree_errors:
        print(f"   [FAIL] {err}")

    print(f"2. Kanonik Kütük ve Anlamsal Bütünlük: {'BAŞARILI' if not reg_errors else f'{len(reg_errors)} HATA'}")
    for err in reg_errors:
        print(f"   [FAIL] {err}")

    print(f"3. Yapılandırma ve Şema Güvenliği: {'BAŞARILI' if not cfg_errors else f'{len(cfg_errors)} HATA'}")
    for err in cfg_errors:
        print(f"   [FAIL] {err}")

    print("-" * 50)
    if not total_errors:
        print("SONUÇ: P00 KANONİK DOĞRULAMA TAMAMEN BAŞARILI (EXECUTED_PASS)")
        print("Bilgi Durumu: G0=NOT_APPROVED, 31 DECISION_REQUIRED, 8 OPEN BLOCKERS, 10 TC NOT_RUN")
        return 0
    else:
        print(f"SONUÇ: P00 KANONİK DOĞRULAMA BAŞARISIZ ({len(total_errors)} hata)")
        return 1


if __name__ == "__main__":
    sys.exit(run_validation())
