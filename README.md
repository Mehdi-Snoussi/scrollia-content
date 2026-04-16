# scrollia-content

Novel catalog for the Scrollia reader app.

## Structure

- `catalog/` — the master novel index (`index.json`)
- `novels/` — per-novel folders; each contains `meta.json` and encrypted chapter files (`ch001.json` ... `ch050.json`)
- `covers/` — cover images (JPG/WebP)
- `avatars/` — author-persona avatars
- `rankings/` — weekly/seasonal top lists
- `promo/` — banner configs
- `scripts/` — the `encrypt_chapter.py` tool used to encrypt plaintext chapters before commit

## Consumption

The Scrollia app reads this repo through the jsDelivr CDN:
`https://cdn.jsdelivr.net/gh/Mehdi-Snoussi/scrollia-content@main/...`

All chapter content is AES-256-CBC encrypted. The decryption key is embedded in the app binary.

## Never commit

- The master encryption key (set via `SCROLLIA_KEY` env var only)
- Plaintext chapter content — run `scripts/encrypt_chapter.py` first
- `.env` files or anything matching `.gitignore` patterns
