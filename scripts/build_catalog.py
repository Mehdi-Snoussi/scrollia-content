#!/usr/bin/env python3
"""Scan novels/*/meta.json and rebuild catalog/index.json.

Usage:
    python scripts/build_catalog.py

Idempotent — safe to rerun whenever a novel is added or updated.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    novels_dir = Path("novels")
    entries = []

    for meta_path in sorted(novels_dir.glob("*/meta.json")):
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)

        entries.append({
            "id": meta["id"],
            "title": meta["title"],
            "subtitle": meta.get("subtitle", ""),
            "penName": meta.get("penName", ""),
            "genre": meta.get("genre", "billionaireRomance"),
            "coverPath": meta.get("coverPath", ""),
            "totalChapters": meta.get("totalChapters", 50),
            "paywallChapter": meta.get("paywallChapter", 9),
            "subtropes": meta.get("subtropes", []),
        })

    index = {
        "version": 1,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totalNovels": len(entries),
        "novels": entries,
    }

    out = Path("catalog/index.json")
    with out.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"OK: {out} — {len(entries)} novel(s)")


if __name__ == "__main__":
    main()
