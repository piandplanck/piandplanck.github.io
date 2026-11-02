# Pi & Planck website runbook

Live site: https://piandplanck.github.io  (repo piandplanck/piandplanck.github.io, branch main, Pages source: GitHub Actions)

## Layout
- `_src/data/pieces.json`: one entry per piece (id, slug, date, topic, title, title_fa, caption, caption_fa, alt, alt_fa, sources)
- `_src/img/<id>_en.jpg`, `<id>_fa.jpg` (1600x900) and `_t.jpg` thumbnails (640x360)
- `_src/assets/`: logo, favicon, og image, headline font
- `_src/build.py`: standard-library builder -> `_site/`
- `.github/workflows/site.yml`: build and deploy on push, every day 18:00 UTC, and manually

## Daily publishing rule
Week 1 runs Sat 31 Oct to Fri 6 Nov 2026 (moved from 24-30 Oct); later weeks follow Sat to Fri.

The build shows only pieces dated on or before today (Pacific). New pieces can be pushed any time ahead of their date; they stay hidden until their day. The daily build runs at 18:00 UTC (10:00 PST / 11:00 PDT), after the 09:00 and 09:15 posts, and every push also rebuilds.

## Add a piece
1. Add an entry to `_src/data/pieces.json` (captions without the @handle) and the four images.
2. `python3 _src/build.py --out _site --through YYYY-MM-DD` to check locally.
3. `git add -A && git commit -m "Add piece <id>" && git push origin HEAD:main`.

## Rules
Nothing secret in this public repo. No dates printed on graphics. Sources listed on each piece page.

## Downloads
Each piece page offers a 4096x2304 JPG and a PDF per language. Files live in `_src/dl/<id>_<lang>_4096.jpg` and `<id>_<lang>.pdf` (branded versions). Add the 4 files per new piece with the other assets.
