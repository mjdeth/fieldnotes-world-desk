# Fieldnotes — World Desk

A one-image brief of Thursday 19 November 2026's world news (early edition, reporting through 14:00 UTC): Trump, Xi and Putin begin trilateral talks at the APEC summit in Shenzhen; European allies plan Berlin talks backing Kyiv; a report published today details COP31 divisions in Antalya; and the Saudi-led coalition says it dealt with a Houthi missile threat towards Riyadh, with debris damage still being assessed. The lead visual is an original, locally generated illustration — a symbolic conference table with labeled country seats, no stock photos and no third-party artwork. Sources and editorial decisions are documented in [SOURCES.md](SOURCES.md).

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/mjdeth/fieldnotes-world-desk/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/mjdeth/fieldnotes-world-desk/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

## How it works

- `render.py` (Python + Pillow, build time) draws `entry.png` deterministically from vector shapes and text — same code, byte-identical PNG, 1024×1024 RGB. Run it with `python3 render.py`.
- `main.py` (Python standard library only) is the sandbox entrypoint: it copies the committed `entry.png` beside it into the output directory (`$MAKEFUN_OUTPUT_DIR`, default `/output`), creating the directory if needed.
