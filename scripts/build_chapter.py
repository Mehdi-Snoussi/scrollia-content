#!/usr/bin/env python3
"""Convert a plaintext chapter into the JSON format the Flutter app expects.

Usage:
    python scripts/build_chapter.py <novel_id> <chapter_number> <title> <content_file>

Example:
    python scripts/build_chapter.py 001 1 "The Coffee I Owed" novels/001/ch001.txt

Output: writes novels/<novel_id>/ch<NNN>.json with { id, chapter, title, content, wordCount }.
Run scripts/encrypt_chapter.py afterward to encrypt the content field before committing.
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <novel_id> <chapter_number> <title> <content_file>")
        sys.exit(1)

    novel_id = sys.argv[1]
    chapter = int(sys.argv[2])
    title = sys.argv[3]
    content_path = Path(sys.argv[4])

    if not content_path.exists():
        print(f"ERROR: {content_path} not found")
        sys.exit(1)

    content = content_path.read_text(encoding="utf-8").strip()
    word_count = len(content.split())

    out_dir = Path("novels") / novel_id
    out_dir.mkdir(parents=True, exist_ok=True)

    ch_file = out_dir / f"ch{chapter:03d}.json"
    payload = {
        "id": novel_id,
        "chapter": chapter,
        "title": title,
        "content": content,
        "wordCount": word_count,
    }

    with ch_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"OK: {ch_file} ({word_count} words)")


if __name__ == "__main__":
    main()
