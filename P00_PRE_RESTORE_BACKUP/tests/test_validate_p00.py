#!/usr/bin/env python3
"""
test_validate_p00.py — Unit test suite for KampusPTS P00 Validator
"""

import unittest
from pathlib import Path
import sys

# Ensure tools directory is in sys.path
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
        self.assertEqual(len(errors), 0, f"Missing files found in file tree: {errors}")

    def test_requirements_count_and_ids(self):
        req_file = self.root / "docs" / "registries" / "requirements.csv"
        rows, fields = read_csv_rows(req_file)
        self.assertEqual(len(rows), 40, f"Expected 40 requirements, found {len(rows)}")
        ids = [r["Id"] for r in rows]
        for i in range(1, 41):
            self.assertIn(f"REQ-{i:03d}", ids)

    def test_nfr_count_and_ids(self):
        nfr_file = self.root / "docs" / "registries" / "nfr.csv"
        rows, fields = read_csv_rows(nfr_file)
        self.assertEqual(len(rows), 16, f"Expected 16 NFRs, found {len(rows)}")
        ids = [r["Id"] for r in rows]
        for i in range(1, 17):
            self.assertIn(f"NFR-{i:03d}", ids)

    def test_decisions_status_all_required(self):
        dec_file = self.root / "docs" / "registries" / "decisions.csv"
        rows, fields = read_csv_rows(dec_file)
        self.assertEqual(len(rows), 31, f"Expected 31 decisions, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["Status"], "DECISION_REQUIRED", f"{r['Id']} is not DECISION_REQUIRED")
            self.assertEqual(r["DecisionMaker"], "TO_ASSIGN", f"{r['Id']} DecisionMaker is not TO_ASSIGN")
            self.assertEqual(r["DecisionDate"], "TBD", f"{r['Id']} DecisionDate is not TBD")

    def test_blockers_all_open(self):
        blk_file = self.root / "docs" / "registries" / "blockers.csv"
        rows, fields = read_csv_rows(blk_file)
        self.assertEqual(len(rows), 8, f"Expected 8 blockers, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["Status"], "OPEN", f"{r['Id']} is not OPEN")

    def test_test_cases_all_not_run(self):
        tc_file = self.root / "docs" / "registries" / "test-cases.csv"
        rows, fields = read_csv_rows(tc_file)
        self.assertEqual(len(rows), 10, f"Expected 10 test cases, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["Status"], "NOT_RUN", f"{r['Id']} is not NOT_RUN")

    def test_traceability_row_count_and_evidence_none(self):
        tr_file = self.root / "docs" / "registries" / "traceability.csv"
        rows, fields = read_csv_rows(tr_file)
        self.assertEqual(len(rows), 56, f"Expected 56 rows in traceability, found {len(rows)}")
        for r in rows:
            self.assertEqual(r["EvidenceId"], "NONE", f"{r['RequirementId']} must have EvidenceId NONE in P00")

    def test_gates_count_and_g0_not_approved(self):
        gate_file = self.root / "docs" / "registries" / "gates.csv"
        rows, fields = read_csv_rows(gate_file)
        self.assertEqual(len(rows), 10, f"Expected 10 gates, found {len(rows)}")
        g0 = next(r for r in rows if r["GateId"] == "G0")
        self.assertEqual(g0["Status"], "NOT_APPROVED")
        for r in rows:
            if r["GateId"] != "G0":
                self.assertEqual(r["Status"], "NOT_STARTED")

    def test_features_flags_all_false(self):
        errors = validate_config(self.root)
        self.assertEqual(len(errors), 0, f"Config validation errors: {errors}")

    def test_full_validation_passes(self):
        tree_errors = validate_file_tree(self.root)
        reg_errors = validate_registries(self.root)
        cfg_errors = validate_config(self.root)
        total = tree_errors + reg_errors + cfg_errors
        self.assertEqual(total, [], f"Total validation errors: {total}")


if __name__ == "__main__":
    unittest.main()
