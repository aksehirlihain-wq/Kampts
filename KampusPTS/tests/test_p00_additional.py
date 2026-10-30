#!/usr/bin/env python3
"""
test_p00_additional.py — Additional Independent Regression Tests for KampusPTS P00 v1.2
Validates canonical semantic invariants:
1. K-01 = Fiziksel ve Mali Otorite Ayrılığı
2. K-02 = Marka Bağımsızlığı
3. K-12 = Test ve Kanıt Doğruluğu (Veracity)
4. REQ-001 = Kapsam/Yönetişim, REQ-002 = Kurumsal Otorite
5. NFR-001 = Kimlik ve Oturum (domain, target_status, verification)
6. DEC-001 = Kurum türü ve gelir sahibi tüzel kişilik (A/B/C/D)
7. DEC-002 = e-Fatura/e-Arşiv belge türü ve düzenleme zamanı
8. Gate phase ranges G1=P01-P04 to G9=P32-P33
9. Feature flags contract strictly false
"""

import unittest
from pathlib import Path
import sys
import json
import csv

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from validate_p00 import find_project_root, read_csv_rows


class TestP00Additional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = find_project_root()

    def test_invariants_k01_k02_k12(self):
        invariants_file = self.root / "docs" / "governance" / "foundational-invariants.md"
        content = invariants_file.read_text(encoding="utf-8")
        self.assertIn("K-01: Fiziksel ve Mali Otorite Ayrılığı", content)
        self.assertIn("K-02: Marka Bağımsızlığı", content)
        self.assertIn("K-12: Test ve Kanıt Doğruluğu", content)
        self.assertNotIn("72 saatlik yerel arabellek", content)

    def test_requirements_req001_req002(self):
        req_file = self.root / "docs" / "registries" / "requirements.csv"
        rows, _ = read_csv_rows(req_file)
        req1 = next(r for r in rows if r["id"] == "REQ-001")
        self.assertIn("Kapsam", req1["title"])
        self.assertEqual(req1["status"], "DESIGNED")
        req2 = next(r for r in rows if r["id"] == "REQ-002")
        self.assertIn("Kurumsal Otorite", req2["title"])
        self.assertEqual(req2["status"], "DESIGNED")

    def test_nfr_canonical_columns_and_nfr001(self):
        nfr_file = self.root / "docs" / "registries" / "nfr.csv"
        rows, fields = read_csv_rows(nfr_file)
        expected = {"domain", "target_status", "verification"}
        self.assertTrue(expected.issubset(set(fields or [])))
        nfr1 = next(r for r in rows if r["id"] == "NFR-001")
        self.assertIn("Kimlik", nfr1["title"])
        self.assertEqual(nfr1["verification"], "NOT_RUN")

    def test_dec_001_and_dec_002(self):
        dec_file = self.root / "docs" / "registries" / "decisions.csv"
        rows, _ = read_csv_rows(dec_file)
        dec1 = next(r for r in rows if r["id"] == "DEC-001")
        self.assertIn("gelir sahibi", dec1["title"].lower())
        opts = dec1["options"]
        self.assertIn("A Üniversite", opts)
        self.assertIn("B Döner sermaye", opts)
        self.assertIn("C Özel işletmeci", opts)
        self.assertIn("D Çoklu tüzel kişilik", opts)
        dec2 = next(r for r in rows if r["id"] == "DEC-002")
        self.assertIn("e-Fatura", dec2["title"])

    def test_gate_semantic_phase_ranges(self):
        gate_file = self.root / "docs" / "registries" / "gates.csv"
        rows, _ = read_csv_rows(gate_file)
        gate_map = {r["id"]: r["phase_range"] for r in rows}
        self.assertEqual(gate_map["G0"], "P00")
        self.assertIn("P01", gate_map["G1"])
        self.assertIn("P04", gate_map["G1"])
        self.assertIn("P05", gate_map["G2"])
        self.assertIn("P06", gate_map["G2"])
        self.assertIn("P07", gate_map["G3"])
        self.assertIn("P10", gate_map["G3"])
        self.assertIn("P11", gate_map["G4"])
        self.assertIn("P15", gate_map["G4"])
        self.assertIn("P16", gate_map["G5"])
        self.assertIn("P19", gate_map["G5"])
        self.assertIn("P20", gate_map["G6"])
        self.assertIn("P22", gate_map["G6"])
        self.assertIn("P23", gate_map["G7"])
        self.assertIn("P28", gate_map["G7"])
        self.assertIn("P29", gate_map["G8"])
        self.assertIn("P31", gate_map["G8"])
        self.assertIn("P32", gate_map["G9"])
        self.assertIn("P33", gate_map["G9"])

    def test_features_contract_zero_live(self):
        cfg_file = self.root / "config" / "features.example.json"
        with open(cfg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        features = data["features"]
        self.assertFalse(features["gateRealCommandsEnabled"])
        self.assertFalse(features["paymentRealCaptureEnabled"])
        self.assertFalse(features["eDocumentRealIssueEnabled"])
        self.assertFalse(features["erpRealPostingEnabled"])
        self.assertFalse(features["multiEntitySplitSettlementEnabled"])


if __name__ == "__main__":
    unittest.main()
