#!/usr/bin/env python3
"""
test_validate_p00.py — Canonical unit test suite for KampusPTS P00 Validator
"""

import unittest
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from validate_p00 import (
    find_project_root,
    validate_file_tree,
    validate_registries,
    validate_config,
    read_csv_rows,
)


class TestValidateP00(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = find_project_root()

    def test_project_root_located(self):
        self.assertTrue(self.root.exists(), "Project root could not be located")
        self.assertTrue((self.root / "docs" / "registries").exists(), "docs/registries not found in root")

    def test_file_tree_completeness(self):
        errors = validate_file_tree(self.root)
        self.assertEqual(len(errors), 0, f"Missing files in tree: {errors}")

    def test_requirements_canonical_schema_and_status(self):
        req_file = self.root / "docs" / "registries" / "requirements.csv"
        rows, fields = read_csv_rows(req_file)
        self.assertEqual(len(rows), 40, f"Expected 40 requirements, found {len(rows)}")
        expected_cols = {"id", "phase", "title", "requirement", "acceptance", "status", "owner_role", "gate"}
        self.assertTrue(expected_cols.issubset(set(fields or [])), f"Missing fields: {fields}")
        for r in rows:
            self.assertEqual(r["status"], "DESIGNED", f"{r['id']} must be DESIGNED")
        req1 = next(r for r in rows if r["id"] == "REQ-001")
        self.assertIn("Kapsam", req1["title"])

    def test_nfr_canonical_schema_and_status(self):
        nfr_file = self.root / "docs" / "registries" / "nfr.csv"
        rows, fields = read_csv_rows(nfr_file)
        self.assertEqual(len(rows), 16, f"Expected 16 NFRs, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["status"], "NOT_RUN", f"{r['id']} must be NOT_RUN in P00")
        nfr1 = next(r for r in rows if r["id"] == "NFR-001")
        self.assertIn("Kimlik", nfr1["title"])

    def test_decisions_canonical_and_models(self):
        dec_file = self.root / "docs" / "registries" / "decisions.csv"
        rows, fields = read_csv_rows(dec_file)
        self.assertEqual(len(rows), 31, f"Expected 31 decisions, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["status"], "DECISION_REQUIRED", f"{r['id']} must be DECISION_REQUIRED")
            self.assertEqual(r["actual_owner"], "TO_ASSIGN", f"{r['id']} actual_owner must be TO_ASSIGN")
            self.assertEqual(r["due_date"], "TBD", f"{r['id']} due_date must be TBD")
            self.assertEqual(r["evidence"], "NONE", f"{r['id']} evidence must be NONE")
        dec1 = next(r for r in rows if r["id"] == "DEC-001")
        opts = dec1["options"]
        self.assertIn("A Üniversite", opts)
        self.assertIn("B Döner sermaye", opts)
        self.assertIn("C Özel işletmeci", opts)
        self.assertIn("D Çoklu tüzel kişilik", opts)

    def test_blockers_all_open_and_canonical_columns(self):
        blk_file = self.root / "docs" / "registries" / "blockers.csv"
        rows, fields = read_csv_rows(blk_file)
        self.assertEqual(len(rows), 8, f"Expected 8 blockers, found {len(rows)}")
        expected_cols = {"id", "phase", "title", "decision_ids", "requirement_ids", "gates", "blocks", "status"}
        self.assertTrue(expected_cols.issubset(set(fields or [])))
        for r in rows:
            self.assertEqual(r["status"], "OPEN")

    def test_test_cases_all_not_run_and_evidence_none(self):
        tc_file = self.root / "docs" / "registries" / "test-cases.csv"
        rows, fields = read_csv_rows(tc_file)
        self.assertEqual(len(rows), 10, f"Expected 10 test cases, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["status"], "NOT_RUN")
            self.assertEqual(r["evidence"], "NONE")

    def test_traceability_row_count_and_status(self):
        tr_file = self.root / "docs" / "registries" / "traceability.csv"
        rows, fields = read_csv_rows(tr_file)
        self.assertEqual(len(rows), 56, f"Expected 56 rows in traceability, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["status"], "DESIGNED_NOT_TESTED")
            self.assertEqual(r["evidence_id"], "NONE")

    def test_gates_canonical_phases_and_g0_not_approved(self):
        gate_file = self.root / "docs" / "registries" / "gates.csv"
        rows, fields = read_csv_rows(gate_file)
        self.assertEqual(len(rows), 10, f"Expected 10 gates, found {len(rows)}")
        g0 = next(r for r in rows if r["id"] == "G0")
        self.assertEqual(g0["status"], "NOT_APPROVED")
        self.assertEqual(g0["phase_range"], "P00")
        g1 = next(r for r in rows if r["id"] == "G1")
        self.assertIn("P01", g1["phase_range"])
        self.assertIn("P04", g1["phase_range"])
        g9 = next(r for r in rows if r["id"] == "G9")
        self.assertIn("P32", g9["phase_range"])
        self.assertIn("P33", g9["phase_range"])
        for r in rows:
            if r["id"] != "G0":
                self.assertEqual(r["status"], "NOT_STARTED")

    def test_features_canonical_schema_and_flags_all_false(self):
        errors = validate_config(self.root)
        self.assertEqual(len(errors), 0, f"Config validation errors: {errors}")

    def test_full_canonical_validation_passes(self):
        tree_errors = validate_file_tree(self.root)
        reg_errors = validate_registries(self.root)
        cfg_errors = validate_config(self.root)
        total = tree_errors + reg_errors + cfg_errors
        self.assertEqual(total, [], f"Total canonical validation errors: {total}")


if __name__ == "__main__":
    unittest.main()
