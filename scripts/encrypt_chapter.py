#!/usr/bin/env python3
"""Encrypt chapter content before committing to public repo."""

import os
import sys
import json
import base64
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY_HEX = os.environ.get('SCROLLIA_KEY')
if not KEY_HEX:
    print("ERROR: Set SCROLLIA_KEY env var")
    sys.exit(1)

KEY = bytes.fromhex(KEY_HEX)
assert len(KEY) == 32, "Key must be 32 bytes (64 hex chars)"

def encrypt_content(plaintext: str) -> dict:
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    padded = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded)
    return {
        'content_enc': base64.b64encode(encrypted).decode(),
        'iv': iv.hex(),
    }

def process_chapter(filepath: Path):
    with filepath.open('r', encoding='utf-8') as f:
        ch = json.load(f)

    if 'content' not in ch:
        print(f"SKIP: {filepath} (already encrypted)")
        return

    enc = encrypt_content(ch['content'])
    del ch['content']
    ch['content_enc'] = enc['content_enc']
    ch['iv'] = enc['iv']
    ch['cipher'] = 'AES-256-CBC'

    with filepath.open('w', encoding='utf-8') as f:
        json.dump(ch, f, indent=2, ensure_ascii=False)

    print(f"OK: {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Batch mode
        for novel_dir in Path('novels').iterdir():
            if not novel_dir.is_dir():
                continue
            for ch_file in novel_dir.glob('ch*.json'):
                process_chapter(ch_file)
    else:
        # Single file
        process_chapter(Path(sys.argv[1]))
