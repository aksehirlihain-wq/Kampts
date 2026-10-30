#!/usr/bin/env python3
"""
build_manifest.py — Computes canonical SHA-256 signatures for KampusPTS files
and outputs manifest.sha256 in the project root.
Excludes: manifest.sha256 itself, .git, cache, pycache, .DS_Store, and binary build artifacts.
"""

import hashlib
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


EXCLUDE_PATTERNS = {
    "manifest.sha256",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "node_modules",
    "bin",
    "obj",
    "dist"
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = find_project_root()
    manifest_path = root / "manifest.sha256"

    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_PATTERNS]
        for f in filenames:
            if f in EXCLUDE_PATTERNS or f.endswith((".pyc", ".tmp", ".zip")):
                continue
            full_path = Path(dirpath) / f
            rel_path = full_path.relative_to(root).as_posix()
            sha = compute_sha256(full_path)
            entries.append((sha, rel_path))

    # Sort entries for deterministic output
    entries.sort(key=lambda x: x[1])

    with open(manifest_path, "w", encoding="utf-8") as out:
        for sha, rel in entries:
            out.write(f"{sha}  {rel}\n")

    print(f"Manifest written successfully: {manifest_path} ({len(entries)} files hashed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
